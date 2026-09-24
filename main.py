"""Система учёта договоров.

Начальный сценарий ПР1: регистрация договора, проверка срока действия
и расчёт итоговой суммы с учётом НДС.
"""

from datetime import date

# Налоговая ставка НДС, %
VAT_RATE = 20


def validate_contract(number, contractor, amount):
    """Проверяет корректность данных договора.

    Возвращает True, если данные корректны, иначе False.
    """
    if not number:
        return False
    if not contractor:
        return False
    if amount <= 0:
        return False
    return True


def get_contract_status(end_date, current_date=None):
    """Определяет статус договора по дате окончания."""
    if current_date is None:
        current_date = date.today()

    if end_date < current_date:
        return "Просрочен"
    if end_date == current_date:
        return "Истекает сегодня"
    return "Действует"


def calculate_total_amount(amount, vat_rate=VAT_RATE):
    """Считает итоговую сумму договора с учётом НДС."""
    vat = amount * vat_rate / 100
    return amount + vat


def main():
    # Данные договора (простые типы данных)
    contract_number = "Д-2026/015"
    contractor = "ООО «Ромашка»"
    amount = 150000.0            # сумма без НДС, руб.
    start_date = date(2026, 9, 1)
    end_date = date(2026, 12, 31)

    # 1. Проверка корректности данных
    if not validate_contract(contract_number, contractor, amount):
        print("Ошибка: данные договора заполнены неверно.")
        return

    # 2. Расчёт суммы с НДС
    total = calculate_total_amount(amount)

    # 3. Определение статуса
    status = get_contract_status(end_date)

    # Вывод результата
    print("=== Карточка договора ===")
    print(f"Номер договора:   {contract_number}")
    print(f"Контрагент:       {contractor}")
    print(f"Дата заключения:  {start_date}")
    print(f"Дата окончания:   {end_date}")
    print(f"Сумма без НДС:    {amount:.2f} руб.")
    print(f"Сумма с НДС {VAT_RATE}%: {total:.2f} руб.")
    print(f"Статус договора:  {status}")


if __name__ == "__main__":