"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json
import os

DATA_DIR = "data"


def _ensure_data_dir() -> None:
    """Создать каталог data, если его нет."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_contracts(filename: str = "contracts.json") -> list[dict]:
    """Загрузить договоры из JSON-файла."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка загрузки договоров: {error}")
        return []


def save_contracts(contracts: list[dict], filename: str = "contracts.json") -> None:
    """Сохранить договоры в JSON-файл."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(contracts, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка сохранения договоров: {error}")


def load_payments(filename: str = "payments.json") -> list[dict]:
    """Загрузить платежи из JSON-файла."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка загрузки платежей: {error}")
        return []


def save_payments(payments: list[dict], filename: str = "payments.json") -> None:
    """Сохранить платежи в JSON-файл."""
    _ensure_data_dir()
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(payments, file, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"Ошибка сохранения платежей: {error}")