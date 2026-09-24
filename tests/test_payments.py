"""Тесты класса Payment."""

from models import Contract, Contractor, Payment
from models.payments import add_payment


def test_payment_creation():
    contractor = Contractor(1, "ООО Ромашка", "7701234567")
    contract = Contract(1, "Д-1", contractor, 1000, "01.01.2026", "31.12.2026")
    payment = Payment(1, contract, 500, "15.01.2026")
    assert payment.id == 1
    assert payment.contract is contract
    assert payment.amount == 500
    assert "Д-1" in str(payment)


def test_add_payment():
    contractor = Contractor(1, "ООО Ромашка", "7701234567")
    contract = Contract(1, "Д-1", contractor, 1000, "01.01.2026", "31.12.2026")
    payments = []
    add_payment(payments, contract, 500, "15.01.2026")
    assert len(payments) == 1