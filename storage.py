"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json
import os

from models import Contract, Contractor, Payment
from models.contractors import find_contractor_by_id
from models.contracts import find_contract

DATA_DIR = "data"


def _ensure_data_dir() -> None:
    """Создать каталог data, если его нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_contractors(filename: str = "contractors.json") -> list[Contractor]:
    """Загрузить контрагентов из JSON-файла."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return [Contractor.from_data(item) for item in data]
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка загрузки контрагентов: {error}")
        return []


def save_contractors(
    contractors: list[Contractor],
    filename: str = "contractors.json",
) -> None:
    """Сохранить контрагентов в JSON-файл."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump([c.to_data() for c in contractors], file,
                      ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка сохранения контрагентов: {error}")


def load_contracts(
    contractors: list[Contractor],
    filename: str = "contracts.json",
) -> list[Contract]:
    """Загрузить договоры из JSON-файла."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка загрузки договоров: {error}")
        return []
    contracts: list[Contract] = []
    for item in data:
        contractor = find_contractor_by_id(contractors, item["contractor_id"])
        if contractor is None:
            continue
        contracts.append(Contract.from_data(item, contractor))
    return contracts


def save_contracts(
    contracts: list[Contract],
    filename: str = "contracts.json",
) -> None:
    """Сохранить договоры в JSON-файл."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump([c.to_data() for c in contracts], file,
                      ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка сохранения договоров: {error}")


def load_payments(
    contracts: list[Contract],
    filename: str = "payments.json",
) -> list[Payment]:
    """Загрузить платежи из JSON-файла."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка загрузки платежей: {error}")
        return []
    payments: list[Payment] = []
    for item in data:
        contract = find_contract_by_id(contracts, item["contract_id"])
        if contract is None:
            continue
        payments.append(Payment.from_data(item, contract))
    return payments


def save_payments(
    payments: list[Payment],
    filename: str = "payments.json",
) -> None:
    """Сохранить платежи в JSON-файл."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump([p.to_data() for p in payments], file,
                      ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка сохранения платежей: {error}")