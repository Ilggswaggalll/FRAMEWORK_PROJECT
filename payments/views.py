"""Страницы платежей."""

from django.shortcuts import render

from .models import Payment


def payments(request):
    """Список платежей со ссылками на договоры."""
    rows = Payment.objects.select_related("contract").order_by("-payment_date", "pk")
    return render(request, "payments/payment_list.html", {"payments": rows})
