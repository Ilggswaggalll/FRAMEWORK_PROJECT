"""Подключение к базе данных SQLite."""

import sqlite3

DB_PATH = "data/contracts.sqlite"


def get_connection() -> sqlite3.Connection:
    """Создать соединение с базой данных с проверкой внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn