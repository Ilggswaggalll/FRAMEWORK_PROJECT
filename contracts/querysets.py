import re

from django.db import models
from django.db.models import Q
from django.utils import timezone


class ContractStatus(models.TextChoices):
    ACTIVE = "active", "Действует"
    TODAY = "today", "Истекает сегодня"
    OVERDUE = "overdue", "Просрочен"
    TERMINATED = "terminated", "Расторгнут"


def status_condition(status, today):
    open_contract = Q(is_terminated=False)
    return {
        ContractStatus.ACTIVE: open_contract & Q(end_date__gt=today),
        ContractStatus.TODAY: open_contract & Q(end_date=today),
        ContractStatus.OVERDUE: open_contract & Q(end_date__lt=today),
        ContractStatus.TERMINATED: Q(is_terminated=True),
    }[status]


class ContractQuerySet(models.QuerySet):
    def with_contractor(self):
        return self.select_related("contractor")

    def search(self, text, *, number_only=False):
        # The SQLite backend supports case-insensitive Cyrillic matching via REGEXP.
        pattern = re.escape(text)
        by_number = Q(number__iregex=pattern)
        if number_only:
            return self.filter(by_number)
        return self.filter(by_number | Q(contractor__name__iregex=pattern))

    def with_status(self, status):
        return self.filter(status_condition(status, timezone.localdate()))
