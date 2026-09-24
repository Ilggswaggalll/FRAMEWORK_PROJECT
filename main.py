"""Система учёта договоров.

ПР2: консольное приложение с меню, коллекциями, модулями,
обработкой исключений и сохранением данных в JSON.
"""

from datetime import date

from contracts import (
    add_contract,
    calculate_total_amount,
    find_contract,
    filter_contracts_by_status,
    get_contract_status,
    get_total_amount,
    sort_contracts_by_amount,
    VAT_RATE,
)
from storage import load_contracts, save_contracts
from utils import input_date, input_float, input_non_empty


def show_contracts(contracts: list[dict]) -> None:
    """Вывести список договоров."""
    if not contracts:
        print("Список договоров пуст.")
        return
    print("\n=== Список договоров ===")
    for contract in contracts:
        status = get_contract_status(contract["end_date"])
        total = calculate_total_amount(contract["amount"])
        print(f"[{contract['number']}] {contract['contractor']} | "
              f"{contract['start_date']} – {contract['end_date']} | "
              f"{contract['amount']:.2f} руб. + НДС = {total:.2f} руб. | "
              f"Статус: {status}")


def show_statistics(contracts: list[dict]) -> None:
    """Вывести статистику по договорам."""
    if not contracts:
        print("Нет данных для статистики.")
        return
    total = get_total_amount(contracts)
    print(f"\nВсего договоров: {len(contracts)}")
    print(f"Общая сумма с НДС: {total:.2f} руб.")


def main() -> None:
    """Точка запуска приложения."""
    contracts = load_contracts()

    menu = (
        "\n=== Система учёта договоров ===\n"
        "1. Показать все договоры\n"
        "2. Добавить договор\n"
        "3. Найти договор по номеру\n"
        "4. Показать просроченные договоры\n"
        "5. Показать статистику\n"
        "6. Сортировать по сумме\n"
        "0. Выход\n"
    )

    while True:
        print(menu)
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_contracts(contracts)

        elif choice == "2":
            number = input_non_empty("Номер договора: ")
            contractor = input_non_empty("Контрагент: ")
            amount = input_float("Сумма без НДС: ")
            start_date = input_date("Дата заключения (ДД.ММ.ГГГГ): ")
            end_date = input_date("Дата окончания (ДД.ММ.ГГГГ): ")
            contract = add_contract(
                contracts, number, contractor, amount, start_date, end_date
            )
            if contract:
                save_contracts(contracts)
                print("Договор добавлен.")

        elif choice == "3":
            number = input_non_empty("Номер договора: ")
            contract = find_contract(contracts, number)
            if contract:
                show_contracts([contract])
            else:
                print("Договор не найден.")

        elif choice == "4":
            overdue = filter_contracts_by_status(contracts, "Просрочен")
            show_contracts(overdue)

        elif choice == "5":
            show_statistics(contracts)

        elif choice == "6":
            sorted_contracts = sort_contracts_by_amount(contracts)
            show_contracts(sorted_contracts)

        elif choice == "0":
            print("Выход из программы.")
            break

        else:
            print("Ошибка: неизвестная команда.")


if __name__ == "__main__":
    main()