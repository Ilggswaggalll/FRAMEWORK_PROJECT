"""Страницы платежей."""

from django.shortcuts import render

from storage import load_contractors, load_contracts, load_payments


def payments(request):
    """Список платежей."""
    contractors_list = load_contractors()
    contracts_list = load_contracts(contractors_list)
    payments_list = load_payments(contracts_list)
    context = {"payments": payments_list}
    return render(request, "payments/payment_list.html", context)