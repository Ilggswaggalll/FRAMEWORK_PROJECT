"""Страницы договоров (данные из SQLite)."""

from django.shortcuts import render

from db.database import get_connection


def contracts(request):
    """Список договоров со статусом и суммой с НДС (расчёт в SQL)."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT contracts.id,
               contracts.number,
               contractors.id AS contractor_id,
               contractors.name  AS contractor_name,
               contracts.amount,
               contracts.start_date,
               contracts.end_date,
               ROUND(contracts.amount * 1.2, 2) AS total_amount,
               CASE
                   WHEN contracts.end_date < DATE('now')
                       THEN 'Просрочен'
                   WHEN contracts.end_date = DATE('now')
                       THEN 'Истекает сегодня'
                   ELSE 'Действует'
               END AS status
        FROM contracts
        JOIN contractors ON contracts.contractor_id = contractors.id
        ORDER BY contracts.number
    """).fetchall()
    conn.close()
    return render(
        request, "contracts/contract_list.html", {"contracts": rows}
    )


def contract_detail(request, contract_id):
    """Карточка договора."""
    conn = get_connection()
    contract = conn.execute(
        """
        SELECT contracts.id,
               contracts.number,
               contractors.name  AS contractor_name,
               contractors.id    AS contractor_id,
               contracts.amount,
               contracts.start_date,
               contracts.end_date,
               ROUND(contracts.amount * 1.2, 2) AS total_amount,
               CASE
                   WHEN contracts.end_date < DATE('now')
                       THEN 'Просрочен'
                   WHEN contracts.end_date = DATE('now')
                       THEN 'Истекает сегодня'
                   ELSE 'Действует'
               END AS status
        FROM contracts
        JOIN contractors ON contracts.contractor_id = contractors.id
        WHERE contracts.id = ?
        """,
        (contract_id,),
    ).fetchone()
    conn.close()
    return render(
        request,
        "contracts/contract_detail.html",
        {"contract": contract},
        status=404 if contract is None else 200,
    )


def overdue_contracts(request):
    """Просроченные договоры (end_date < текущей даты)."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT contracts.id,
               contracts.number,
               contractors.name AS contractor_name,
               contracts.end_date,
               contracts.amount,
               ROUND(contracts.amount * 1.2, 2) AS total_amount
        FROM contracts
        JOIN contractors ON contracts.contractor_id = contractors.id
        WHERE contracts.end_date < DATE('now')
        ORDER BY contracts.end_date
    """).fetchall()
    conn.close()
    return render(
        request,
        "contracts/overdue_list.html",
        {"contracts": rows},
    )


def statistics(request):
    """Статистика по контрагентам: договоры и суммы."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT contractors.name AS contractor_name,
               COUNT(contracts.id) AS contracts_count,
               COALESCE(SUM(contracts.amount), 0) AS total_amount
        FROM contractors
        LEFT JOIN contracts ON contracts.contractor_id = contractors.id
        GROUP BY contractors.id, contractors.name
        ORDER BY contracts_count DESC, total_amount DESC
    """).fetchall()
    conn.close()
    return render(
        request, "contracts/statistics.html", {"statistics": rows}
    )