"""Страницы договоров."""

from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils import timezone

from contractors.models import Contractor

from .forms import SORT_ORDERS, ContractFilterForm, ContractForm
from .models import Contract
from .querysets import ContractStatus, status_condition


def contracts(request):
    """Список договоров со статусом и суммой с НДС."""
    form = ContractFilterForm(request.GET)
    form.is_valid()
    filters = form.cleaned_data
    rows = Contract.objects.with_contractor()
    if search := filters.get("q"):
        rows = rows.search(search, number_only=filters.get("search_scope") == "number")
    if contractor := filters.get("contractor"):
        rows = rows.filter(contractor=contractor)
    if status := filters.get("status"):
        rows = rows.with_status(status)

    if end_before := filters.get("end_before"):
        rows = rows.filter(end_date__lte=end_before)

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
    contract = Contract.objects.with_contractor().filter(pk=contract_id).first()
    return render(
        request,
        "contracts/contract_detail.html",
        {"contract": contract},
        status=404 if contract is None else 200,
    )


def overdue_contracts(request):
    """Договоры, срок которых истёк до сегодняшнего дня."""
    rows = (
        Contract.objects.with_contractor()
        .with_status(ContractStatus.OVERDUE)
        .order_by("end_date", "pk")
    )
    return render(request, "contracts/overdue_list.html", {"contracts": rows})


def statistics(request):
    """Количество договоров и сумма без НДС для каждого контрагента."""
    rows = Contractor.objects.values("pk", "name").annotate(
        contracts_count=Count("contracts"),
        total_amount=Sum("contracts__amount", default=0),
    ).order_by("-contracts_count", "-total_amount", "pk")
    today = timezone.localdate()
    totals = Contract.objects.aggregate(
        amount=Sum("amount", default=0),
        **{status.value: Count("pk", filter=status_condition(status, today))
           for status in ContractStatus},
    )
    status_counts = [(status.label, totals[status.value]) for status in ContractStatus]
    return render(
        request, "contracts/statistics.html",
        {"statistics": rows, "total_amount": totals["amount"], "status_counts": status_counts},
    )


@permission_required("contracts.add_contract", login_url="admin:login")
def contract_create(request):
    return contract_form(request)


@permission_required("contracts.change_contract", login_url="admin:login")
def contract_edit(request, contract_id):
    return contract_form(request, get_object_or_404(Contract, pk=contract_id))


def contract_form(request, contract=None):
    if request.method == "POST":
        form = ContractForm(request.POST, request.FILES, instance=contract)
        if form.is_valid():
            return redirect(form.save())
    else:
        form = ContractForm(instance=contract)
    return render(
        request, "contracts/contract_form.html", {"form": form, "contract": contract}
    )


@require_POST
@permission_required("contracts.change_contract", login_url="admin:login")
def contract_terminate(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    if not contract.is_terminated:
        contract.is_terminated = True
        contract.save(update_fields=["is_terminated"])
    return redirect(contract)
