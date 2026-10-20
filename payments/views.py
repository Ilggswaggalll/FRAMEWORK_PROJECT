"""Страницы платежей (данные из SQLite)."""

from django.shortcuts import render

from db.database import get_connection


def payments(request):
    """Список платежей с номером договора и контрагентом."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT payments.id,
               payments.amount,
               payments.payment_date,
               contracts.id      AS contract_id,
               contracts.number  AS contract_number,
               contractors.name  AS contractor_name
        FROM payments
        JOIN contracts   ON payments.contract_id  = contracts.id
        JOIN contractors ON contracts.contractor_id = contractors.id
        ORDER BY payments.payment_date DESC
    """).fetchall()
    conn.close()
    return render(
        request, "payments/payment_list.html", {"payments": rows}
    )