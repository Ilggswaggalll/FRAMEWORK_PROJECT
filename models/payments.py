"""Платежи: класс Payment и функции обработки коллекции."""

from __future__ import annotations

from .contracts import Contract


class Payment:
    """Платёж по договору."""

    def __init__(
        self,
        payment_id: int,
        contract: Contract,
        amount: float,
        payment_date: str,
    ) -> None:
        """Создать платёж."""
        self.id = payment_id
        self.contract = contract
        self.amount = amount
        self.payment_date = payment_date

    def __str__(self) -> str:
        """Строковое представление платежа."""
        return (
            f"[{self.id}] по договору {self.contract.number} | "
            f"{self.amount:.2f} руб. | {self.payment_date}"
        )

    @classmethod
    def from_data(cls, data: dict, contract: Contract) -> "Payment":
        """Создать платёж из словаря и найденного договора."""
        return cls(
            payment_id=data["id"],
            contract=contract,
            amount=data["amount"],
            payment_date=data["payment_date"],
        )

    def to_data(self) -> dict:
        """Преобразовать платёж в словарь для JSON."""
        return {
            "id": self.id,
            "contract_id": self.contract.id,
            "amount": self.amount,
            "payment_date": self.payment_date,
        }


def add_payment(
    payments: list[Payment],
    contract: Contract,
    amount: float,
    payment_date: str,
) -> Payment:
    """Создать платёж и добавить его в коллекцию."""
    new_id = max((p.id for p in payments), default=0) + 1
    payment = Payment(new_id, contract, amount, payment_date)
    payments.append(payment)
    return payment


def show_payments(payments: list[Payment]) -> None:
    """Вывести список платежей."""
    if not payments:
        print("Список платежей пуст.")
        return
    print("\n=== Платежи ===")
    for payment in payments:
        print(payment)