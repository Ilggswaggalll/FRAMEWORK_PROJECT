"""Страницы контрагентов (данные из SQLite)."""

from django.shortcuts import render

from db.database import get_connection


def contractors(request):
    """Список контрагентов."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT id, name, inn
        FROM contractors
        ORDER BY name
    """).fetchall()
    conn.close()
    return render(
        request, "contractors/contractor_list.html", {"contractors": rows}
    )


def contractor_detail(request, contractor_id):
    """Карточка контрагента."""
    conn = get_connection()
    contractor = conn.execute(
        """
        SELECT id, name, inn
        FROM contractors
        WHERE id = ?
        """,
        (contractor_id,),
    ).fetchone()
    conn.close()
    return render(
        request,
        "contractors/contractor_detail.html",
        {"contractor": contractor},
        status=404 if contractor is None else 200,
    )