"""Система учёта договоров.

ПР3: объектная модель — классы Contract, Contractor, Payment.
"""

from models import Contract, Contractor, Payment
from models.contractors import (
    add_contractor,
    find_contractor,
    show_contractors,
)
from models.contracts import (
    add_contract,
    filter_contracts_by_status,
    find_contract,
    get_total_amount,
    show_contracts,
    sort_contracts_by_amount,
)
from models.payments import add_payment, show_payments
from storage import (
    load_contractors,
    load_contracts,
    load_payments,
    save_contractors,
    save_contracts,
    save_payments,
)
from utils import input_date, input_float, input_int, input_non_empty


def create_new_contract(
    contracts: list[Contract],
    contractors: list[Contractor],
) -> None:
    """Создать договор через меню."""
    if not contractors:
        print("Сначала добавьте хотя бы одного контрагента.")
        return
    show_contractors(contractors)
    contractor_id = input_int("ID контрагента: ")
    contractor = None
    for c in contractors:
        if c.id == contractor_id:
            contractor = c
            break
    if contractor is None:
        print("Контрагент не найден.")
        return
    number = input_non_empty("Номер договора: ")
    amount = input_float("Сумма без НДС: ")
    start_date = input_date("Дата заключения (ДД.ММ.ГГГГ): ")
    end_date = input_date("Дата окончания (ДД.ММ.ГГГГ): ")
    contract = add_contract(
        contracts, number, contractor, amount, start_date, end_date
    )
    if contract:
        save_contracts(contracts)
        print("Договор добавлен.")


def create_new_payment(
    payments: list[Payment],
    contracts: list[Contract],
) -> None:
    """Создать платёж через меню."""
    if not contracts:
        print("Сначала добавьте хотя бы один договор.")
        return
    show_contracts(contracts)
    contract_id = input_int("ID договора: ")
    contract = None
    for c in contracts:
        if c.id == contract_id:
            contract = c
            break
    if contract is None:
        print("Договор не найден.")
        return
    amount = input_float("Сумма платежа: ")
    payment_date = input_date("Дата платежа (ДД.ММ.ГГГГ): ")
    add_payment(payments, contract, amount, payment_date)
    save_payments(payments)
    print("Платёж добавлен.")


def show_statistics(contracts: list[Contract]) -> None:
    """Вывести статистику по договорам."""
    if not contracts:
        print("Нет данных для статистики.")
        return
    total = get_total_amount(contracts)
    print(f"\nВсего договоров: {len(contracts)}")
    print(f"Общая сумма с НДС: {total:.2f} руб.")


def main() -> None:
    """Точка запуска приложения."""
    contractors = load_contractors()
    contracts = load_contracts(contractors)
    payments = load_payments(contracts)

    menu = (
        "\n=== Система учёта договоров ===\n"
        "1. Показать контрагентов\n"
        "2. Добавить контрагента\n"
        "3. Показать договоры\n"
        "4. Добавить договор\n"
        "5. Найти договор по номеру\n"
        "6. Показать просроченные договоры\n"
        "7. Показать статистику\n"
        "8. Сортировать договоры по сумме\n"
        "9. Показать платежи\n"
        "10. Добавить платёж\n"
        "0. Выход\n"
    )

    while True:
        print(menu)
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_contractors(contractors)

        elif choice == "2":
            name = input_non_empty("Название контрагента: ")
            inn = input_non_empty("ИНН: ")
            add_contractor(contractors, name, inn)
            save_contractors(contractors)
            print("Контрагент добавлен.")

        elif choice == "3":
            show_contracts(contracts)

        elif choice == "4":
            create_new_contract(contracts, contractors)

        elif choice == "5":
            number = input_non_empty("Номер договора: ")
            contract = find_contract(contracts, number)
            if contract:
                show_contracts([contract])
            else:
                print("Договор не найден.")

        elif choice == "6":
            overdue = filter_contracts_by_status(contracts, "Просрочен")
            show_contracts(overdue)

        elif choice == "7":
            show_statistics(contracts)

        elif choice == "8":
            sorted_contracts = sort_contracts_by_amount(contracts)
            show_contracts(sorted_contracts)

        elif choice == "9":
            show_payments(payments)

        elif choice == "10":
            create_new_payment(payments, contracts)

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Ошибка: неизвестная команда.")


if __name__ == "__main__":
    main()