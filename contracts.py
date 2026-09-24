"""Функции для работы с договорами."""

from datetime import date, datetime

VAT_RATE = 20


def validate_contract(number: str, contractor: str, amount: float) -> bool:
    """Проверяет корректность данных договора."""
    if not number or not contractor:
        return False
    if amount <= 0:
        return False
    return True


def get_contract_status(end_date: str, current_date: date | None = None) -> str:
    """Определяет статус договора по дате окончания."""
    if current_date is None:
        current_date = date.today()
    end = datetime.strptime(end_date, "%d.%m.%Y").date()
    if end < current_date:
        return "Просрочен"
    if end == current_date:
        return "Истекает сегодня"
    return "Действует"


def calculate_total_amount(amount: float, vat_rate: float = VAT_RATE) -> float:
    """Считает итоговую сумму договора с учётом НДС."""
    vat = amount * vat_rate / 100
    return amount + vat


def add_contract(contracts: list[dict], number: str, contractor: str,
                 amount: float, start_date: str, end_date: str) -> dict | None:
    """Добавить договор в список."""
    if not validate_contract(number, contractor, amount):
        print("Ошибка: данные договора заполнены неверно.")
        return None
    contract = {
        "number": number,
        "contractor": contractor,
        "amount": amount,
        "start_date": start_date,
        "end_date": end_date,
    }
    contracts.append(contract)
    return contract


def find_contract(contracts: list[dict], number: str) -> dict | None:
    """Найти договор по номеру."""
    for contract in contracts:
        if contract["number"] == number:
            return contract
    return None


def filter_contracts_by_status(contracts: list[dict], status: str) -> list[dict]:
    """Отобрать договоры по статусу."""
    return [c for c in contracts if get_contract_status(c["end_date"]) == status]


def sort_contracts_by_amount(contracts: list[dict]) -> list[dict]:
    """Отсортировать договоры по сумме (возрастание)."""
    return sorted(contracts, key=lambda c: c["amount"])


def get_total_amount(contracts: list[dict]) -> float:
    """Подсчитать общую сумму всех договоров с НДС."""
    return sum(calculate_total_amount(c["amount"]) for c in contracts)