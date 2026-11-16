"""Страницы договоров."""

import re

from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.shortcuts import render
from django.utils import timezone

from contractors.models import Contractor

from .forms import SORT_ORDERS, ContractFilterForm
from .models import Contract


def contracts(request):
    """Список договоров со статусом и суммой с НДС."""
    form = ContractFilterForm(request.GET)
    form.is_valid()
    filters = form.cleaned_data
    rows = Contract.objects.select_related("contractor")

    if search := filters.get("q"):
        # Django's SQLite regex lookup supports case-insensitive Cyrillic matching.
        pattern = re.escape(search)
        if filters.get("search_scope") == "number":
            rows = rows.filter(number__iregex=pattern)
        else:
            rows = rows.filter(Q(number__iregex=pattern) | Q(contractor__name__iregex=pattern))
    contractor = filters.get("contractor")
    today = timezone.localdate()
    status = filters.get("status")
    if contractor and status == "overdue":
        rows = rows.filter(contractor__pk=contractor.pk, end_date__lt=today)
    elif contractor:
        rows = rows.filter(contractor__pk=contractor.pk)
    if status == "active":
        rows = rows.exclude(end_date__lte=today)
    elif status == "today":
        rows = rows.filter(end_date=today)
    elif status == "overdue" and not contractor:
        rows = rows.filter(end_date__lt=today)

    sort = filters.get("sort") or "number"
    rows = rows.order_by(SORT_ORDERS[sort][0], "pk")
    page_obj = Paginator(rows, 3).get_page(request.GET.get("page"))
    return render(
        request,
        "contracts/contract_list.html",
        {"filter_form": form, "page_obj": page_obj, "contracts": page_obj.object_list},
    )


def contract_detail(request, contract_id):
    """Карточка договора."""
    contract = Contract.objects.select_related("contractor").filter(pk=contract_id).first()
    return render(
        request,
        "contracts/contract_detail.html",
        {"contract": contract},
        status=404 if contract is None else 200,
    )


def overdue_contracts(request):
    """Договоры, срок которых истёк до сегодняшнего дня."""
    rows = (
        Contract.objects.select_related("contractor")
        .filter(end_date__lt=timezone.localdate())
        .order_by("end_date", "pk")
    )
    return render(request, "contracts/overdue_list.html", {"contracts": rows})


def statistics(request):
    """Количество договоров и сумма без НДС для каждого контрагента."""
    rows = Contractor.objects.values("pk", "name").annotate(
        contracts_count=Count("contracts"),
        total_amount=Sum("contracts__amount", default=0),
    ).order_by("-contracts_count", "-total_amount", "pk")
    totals = Contract.objects.aggregate(amount=Sum("amount", default=0))
    return render(
        request, "contracts/statistics.html",
        {"statistics": rows, "total_amount": totals["amount"]},
    )
