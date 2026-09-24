"""Тесты класса Contractor."""

from models import Contractor
from models.contractors import add_contractor, find_contractor


def test_contractor_creation():
    contractor = Contractor(1, "ООО Ромашка", "7701234567")
    assert contractor.id == 1
    assert contractor.name == "ООО Ромашка"
    assert contractor.inn == "7701234567"
    assert "ООО Ромашка" in str(contractor)


def test_add_contractor():
    contractors = []
    add_contractor(contractors, "ООО Ромашка", "7701234567")
    assert len(contractors) == 1


def test_find_contractor():
    contractors = []
    add_contractor(contractors, "ООО Ромашка", "7701234567")
    assert find_contractor(contractors, "ромашка")
    assert not find_contractor(contractors, "василёк")