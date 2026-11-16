"""Перенос записей из SQLite-базы ПР7 в модели Django."""

import sqlite3
from contextlib import closing
from datetime import date
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction

from contractors.models import Contractor
from contracts.models import Contract
from payments.models import Payment


class Command(BaseCommand):
    help = "Переносит контрагентов, договоры и платежи из базы ПР7."

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            type=Path,
            default=settings.BASE_DIR / "data" / "contracts.sqlite",
        )

    def handle(self, *args, **options):
        source = options["source"].resolve()
        tables = (
            (Contractor, "SELECT id, name, inn FROM contractors ORDER BY id"),
            (
                Contract,
                "SELECT id, number, contractor_id, amount, start_date, end_date "
                "FROM contracts ORDER BY id",
            ),
            (
                Payment,
                "SELECT id, contract_id, amount, payment_date FROM payments ORDER BY id",
            ),
        )

        results = []
        try:
            with closing(sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)) as legacy:
                legacy.row_factory = sqlite3.Row
                legacy.execute("BEGIN")
                with transaction.atomic():
                    for model, query in tables:
                        rows = legacy.execute(query).fetchall()
                        created = sum(self.import_row(model, row) for row in rows)
                        results.append((model.__name__, created, len(rows) - created))
        except (sqlite3.Error, IntegrityError, ValueError) as error:
            raise CommandError(f"Ошибка импорта из {source}: {error}") from error

        for name, created, existing in results:
            self.stdout.write(f"{name}: добавлено {created}, уже совпадало {existing}")

    @staticmethod
    def import_row(model, row):
        fields = dict(row)
        pk = fields.pop("id")
        for field in ("start_date", "end_date", "payment_date"):
            if field in fields:
                fields[field] = date.fromisoformat(fields[field])
        if "amount" in fields:
            fields["amount"] = Decimal(str(fields["amount"]))

        obj, created = model.objects.get_or_create(pk=pk, defaults=fields)
        if not created and any(getattr(obj, key) != value for key, value in fields.items()):
            raise CommandError(f"{model.__name__} id={pk}: запись в Django отличается от ПР7.")
        return created
