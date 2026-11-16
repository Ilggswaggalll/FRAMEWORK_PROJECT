from django.db import models


class Payment(models.Model):
    contract = models.ForeignKey(
        "contracts.Contract",
        on_delete=models.PROTECT,
        verbose_name="договор",
        related_name="payments",
    )
    amount = models.DecimalField("сумма", max_digits=14, decimal_places=2)
    payment_date = models.DateField("дата платежа")

    class Meta:
        verbose_name = "платёж"
        verbose_name_plural = "платежи"

    def __str__(self):
        return f"Платёж №{self.pk} на {self.amount} ({self.payment_date})"
