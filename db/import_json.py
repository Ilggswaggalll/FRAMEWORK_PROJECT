"""Импорт данных из JSON-файлов в SQLite."""

import json
from datetime import datetime

from db.database import get_connection

CONTRACTORS_FILE = "data/contractors.json"
CONTRACTS_FILE = "data/contracts.json"
PAYMENTS_FILE = "data/payments.json"


def _iso_date(ddmmyyyy: str) -> str:
    """Преобразовать 'ДД.ММ.ГГГГ' → 'ГГГГ-ММ-ДД'."""
    return datetime.strptime(ddmmyyyy, "%d.%m.%Y").date().isoformat()


def load_json(filename: str) -> list[dict]:
    """Прочитать JSON-файл."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_contractors(conn) -> None:
    """Импортировать контрагентов."""
    rows = load_json(CONTRACTORS_FILE)
    conn.executemany(
        """
        INSERT INTO contractors (id, name, inn)
        VALUES (?, ?, ?)
        """,
        [(r["id"], r["name"], r["inn"]) for r in rows],
    )


def import_contracts(conn) -> None:
    """Импортировать договоры."""
    rows = load_json(CONTRACTS_FILE)
    conn.executemany(
        """
        INSERT INTO contracts
            (id, number, contractor_id, amount, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                r["id"],
                r["number"],
                r["contractor_id"],
                float(r["amount"]),
                _iso_date(r["start_date"]),
                _iso_date(r["end_date"]),
            )
            for r in rows
        ],
    )


def import_payments(conn) -> None:
    """Импортировать платежи."""
    rows = load_json(PAYMENTS_FILE)
    conn.executemany(
        """
        INSERT INTO payments (id, contract_id, amount, payment_date)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                r["id"],
                r["contract_id"],
                float(r["amount"]),
                _iso_date(r["payment_date"]),
            )
            for r in rows
        ],
    )


def main() -> None:
    """Выполнить импорт."""
    conn = get_connection()
    try:
        import_contractors(conn)
        import_contracts(conn)
        import_payments(conn)
        conn.commit()
        print("Импорт завершён.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()