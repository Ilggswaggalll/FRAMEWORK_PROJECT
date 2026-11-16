from decimal import ROUND_HALF_UP, Decimal

from django.db import models
from django.utils import timezone


class Contract(models.Model):
    number = models.CharField(max_length=100, unique=True)
    contractor = models.ForeignKey(
        "contractors.Contractor",
        on_delete=models.PROTECT,
        related_name="contracts",
    )
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.number

    @property
    def total_amount(self):
        """Сумма с НДС 20%, округлённая до копеек."""
        return (self.amount * Decimal("1.20")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    @property
    def status(self):
        """Статус договора по дате окончания."""
        today = timezone.localdate()
        if self.end_date < today:
            return "Просрочен"
        if self.end_date == today:
            return "Истекает сегодня"
        return "Действует"
