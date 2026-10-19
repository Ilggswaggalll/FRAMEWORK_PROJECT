"""Страницы договоров."""

from django.shortcuts import render

from models.contracts import find_contract_by_id
from storage import load_contractors, load_contracts


def _load_all():
    """Загрузить договоры (с привязанными контрагентами)."""
    contractors_list = load_contractors()
    return load_contracts(contractors_list)


def contracts(request):
    """Список договоров."""
    contracts_list = _load_all()
    context = {"contracts": contracts_list}
    return render(request, "contracts/contract_list.html", context)


def contract_detail(request, contract_id):
    """Карточка договора."""
    contracts_list = _load_all()
    contract = find_contract_by_id(contracts_list, contract_id)
    context = {"contract": contract}
    return render(
        request,
        "contracts/contract_detail.html",
        context,
        status=404 if contract is None else 200,
    )