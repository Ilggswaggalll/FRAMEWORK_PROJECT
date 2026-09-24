"""Тесты функций работы с договорами."""

from contracts import (
    add_contract,
    calculate_total_amount,
    find_contract,
    get_contract_status,
    validate_contract,
)


def test_validate_contract():
    assert validate_contract("Д-1", "ООО Ромашка", 1000) is True
    assert validate_contract("", "ООО Ромашка", 1000) is False
    assert validate_contract("Д-1", "", 1000) is False
    assert validate_contract("Д-1", "ООО Ромашка", -5) is False


def test_calculate_total_amount():
    assert calculate_total_amount(1000) == 1200.0


def test_get_contract_status():
    assert get_contract_status("01.01.2020") == "Просрочен"
    assert get_contract_status("31.12.2099") == "Действует"


def test_add_and_find_contract():
    contracts = []
    add_contract(contracts, "Д-1", "ООО Ромашка", 1000, "01.01.2026", "31.12.2026")
    assert len(contracts) == 1
    assert find_contract(contracts, "Д-1") is not None
    assert find_contract(contracts, "Д-999") is None