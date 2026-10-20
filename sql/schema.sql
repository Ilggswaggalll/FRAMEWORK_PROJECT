-- =============================================
-- Система учёта договоров: структура базы данных
-- =============================================

CREATE TABLE IF NOT EXISTS contractors (
    id   INTEGER PRIMARY KEY,
    name TEXT    NOT NULL,
    inn  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS contracts (
    id            INTEGER PRIMARY KEY,
    number        TEXT    NOT NULL UNIQUE,
    contractor_id INTEGER NOT NULL,
    amount        REAL    NOT NULL,
    start_date    TEXT    NOT NULL,
    end_date      TEXT    NOT NULL,
    FOREIGN KEY (contractor_id) REFERENCES contractors(id)
);

CREATE TABLE IF NOT EXISTS payments (
    id           INTEGER PRIMARY KEY,
    contract_id  INTEGER NOT NULL,
    amount       REAL    NOT NULL,
    payment_date TEXT    NOT NULL,
    FOREIGN KEY (contract_id) REFERENCES contracts(id)
);