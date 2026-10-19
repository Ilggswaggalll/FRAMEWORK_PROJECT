from django.shortcuts import render

"""Страницы платежей."""

from django.http import HttpResponse

from homepage.views import page
from models.payments import (
    add_payment,
    show_payments,
)
from storage import load_contractors, load_contracts, load_payments


def payments(request):
    """Список платежей."""
    contractors_list = load_contractors()
    contracts_list = load_contracts(contractors_list)
    payments_list = load_payments(contracts_list)

    items = ""
    for p in payments_list:
        items += (
            f'<li class="list-group-item">'
            f'Платёж №{p.id} по договору '
            f'<a href="/contracts/{p.contract.id}/">№{p.contract.number}</a> — '
            f'{p.amount:.2f} руб. — {p.payment_date}'
            f'</li>'
        )
    content = f"""
    <h1>Платежи</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Платежи", content))