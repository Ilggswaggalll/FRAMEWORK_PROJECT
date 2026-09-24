"""Тесты сохранения и загрузки данных."""

import os

from storage import load_contracts, save_contracts


def test_save_and_load_contracts(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    contracts = [{"number": "Д-1", "contractor": "ООО Ромашка",
                  "amount": 1000, "start_date": "01.01.2026",
                  "end_date": "31.12.2026"}]
    save_contracts(contracts)
    loaded = load_contracts()
    assert loaded == contracts


def test_load_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr("storage.DATA_DIR", str(tmp_path))
    assert load_contracts() == []