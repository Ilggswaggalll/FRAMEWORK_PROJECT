from decimal import ROUND_HALF_UP, Decimal

from django.db import models
from django.urls import reverse
from django.utils import timezone

from .querysets import ContractQuerySet, ContractStatus


class Contract(models.Model):
    number = models.CharField("номер", max_length=100, unique=True)
    contractor = models.ForeignKey(
        "contractors.Contractor",
        on_delete=models.PROTECT,
        verbose_name="контрагент",
        related_name="contracts",
    )
    amount = models.DecimalField("сумма без НДС", max_digits=14, decimal_places=2)
    start_date = models.DateField("дата начала")
    end_date = models.DateField("дата окончания")

    image = models.ImageField("изображение", upload_to="contracts/%Y/%m/", blank=True)
    is_terminated = models.BooleanField("расторгнут", default=False)

    objects = ContractQuerySet.as_manager()

    class Meta:
        verbose_name = "договор"
        verbose_name_plural = "договоры"

    def get_absolute_url(self):
        return reverse("contracts:detail", kwargs={"contract_id": self.pk})

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
        if self.is_terminated:
            return ContractStatus.TERMINATED.label
        today = timezone.localdate()
        if self.end_date < today:
            return ContractStatus.OVERDUE.label
        if self.end_date == today:
            return ContractStatus.TODAY.label
        return ContractStatus.ACTIVE.label
