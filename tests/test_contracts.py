"""Тесты класса Contract."""

from models import Contract, Contractor
from models.contracts import (
    add_contract,
    find_contract,
)


def test_contract_creation():
    contractor = Contractor(1, "ООО Ромашка", "7701234567")
    contract = Contract(1, "Д-1", contractor, 1000, "01.01.2026", "31.12.2026")
    assert contract.id == 1
    assert contract.number == "Д-1"
    assert contract.contractor is contractor
    assert contract.total_amount() == 1200.0


def test_contract_status():
    contractor = Contractor(1, "ООО Ромашка", "7701234567")
    contract = Contract(1, "Д-1", contractor, 1000, "01.01.2020", "31.12.2020")
    assert contract.status() == "Просрочен"


def test_add_and_find_contract():
    contractor = Contractor(1, "ООО Ромашка", "7701234567")
    contracts = []
    add_contract(contracts, "Д-1", contractor, 1000, "01.01.2026", "31.12.2026")
    assert len(contracts) == 1
    assert find_contract(contracts, "Д-1") is not None
    assert find_contract(contracts, "Д-999") is None