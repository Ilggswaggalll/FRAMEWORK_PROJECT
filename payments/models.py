from django.db import models


class Payment(models.Model):
    contract = models.ForeignKey(
        "contracts.Contract",
        on_delete=models.PROTECT,
        related_name="payments",
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"{self.contract_id}: {self.amount} ({self.payment_date})"
