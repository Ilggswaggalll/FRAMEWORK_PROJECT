"""Договоры: класс Contract и функции обработки коллекции."""

from __future__ import annotations

from datetime import date, datetime

from .contractors import Contractor

VAT_RATE = 20


class Contract:
    """Договор с контрагентом."""

    def __init__(
        self,
        contract_id: int,
        number: str,
        contractor: Contractor,
        amount: float,
        start_date: str,
        end_date: str,
    ) -> None:
        """Создать договор."""
        self.id = contract_id
        self.number = number
        self.contractor = contractor
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date

    def total_amount(self, vat_rate: float = VAT_RATE) -> float:
        """Итоговая сумма договора с НДС."""
        vat = self.amount * vat_rate / 100
        return self.amount + vat

    def status(self, current_date: date | None = None) -> str:
        """Статус договора по дате окончания."""
        if current_date is None:
            current_date = date.today()
        end = datetime.strptime(self.end_date, "%d.%m.%Y").date()
        if end < current_date:
            return "Просрочен"
        if end == current_date:
            return "Истекает сегодня"
        return "Действует"

    def is_valid(self) -> bool:
        """Проверить корректность данных договора."""
        if not self.number or not self.contractor:
            return False
        if self.amount <= 0:
            return False
        return True

    def __str__(self) -> str:
        """Строковое представление договора."""
        return (
            f"[{self.number}] {self.contractor.name} | "
            f"{self.start_date} – {self.end_date} | "
            f"{self.amount:.2f} руб. + НДС = {self.total_amount():.2f} руб. | "
            f"Статус: {self.status()}"
        )

    @classmethod
    def from_data(cls, data: dict, contractor: Contractor) -> "Contract":
        """Создать договор из словаря и найденного контрагента."""
        return cls(
            contract_id=data["id"],
            number=data["number"],
            contractor=contractor,
            amount=data["amount"],
            start_date=data["start_date"],
            end_date=data["end_date"],
        )

    def to_data(self) -> dict:
        """Преобразовать договор в словарь для JSON."""
        return {
            "id": self.id,
            "number": self.number,
            "contractor_id": self.contractor.id,
            "amount": self.amount,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }


def add_contract(
    contracts: list[Contract],
    number: str,
    contractor: Contractor,
    amount: float,
    start_date: str,
    end_date: str,
) -> Contract | None:
    """Создать договор и добавить его в коллекцию."""
    new_id = max((c.id for c in contracts), default=0) + 1
    contract = Contract(new_id, number, contractor, amount, start_date, end_date)
    if not contract.is_valid():
        print("Ошибка: данные договора заполнены неверно.")
        return None
    contracts.append(contract)
    return contract


def find_contract(contracts: list[Contract], number: str) -> Contract | None:
    """Найти договор по номеру."""
    for contract in contracts:
        if contract.number == number:
            return contract
    return None


def filter_contracts_by_status(
    contracts: list[Contract],
    status: str,
) -> list[Contract]:
    """Отобрать договоры по статусу."""
    return [c for c in contracts if c.status() == status]


def sort_contracts_by_amount(contracts: list[Contract]) -> list[Contract]:
    """Отсортировать договоры по сумме (возрастание)."""
    return sorted(contracts, key=lambda c: c.amount)


def get_total_amount(contracts: list[Contract]) -> float:
    """Подсчитать общую сумму всех договоров с НДС."""
    return sum(c.total_amount() for c in contracts)


def show_contracts(contracts: list[Contract]) -> None:
    """Вывести список договоров."""
    if not contracts:
        print("Список договоров пуст.")
        return
    print("\n=== Список договоров ===")
    for contract in contracts:
        print(contract)


def find_contract_by_id(
    contracts: list[Contract],
    contract_id: int,
) -> Contract | None:
    """Найти договор по id."""
    for contract in contracts:
        if contract.id == contract_id:
            return contract
    return None