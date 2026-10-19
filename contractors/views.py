from django.shortcuts import render

"""Страницы контрагентов."""

from django.http import HttpResponse

from homepage.views import page
from models.contractors import find_contractor_by_id
from storage import load_contractors


def contractors(request):
    """Список контрагентов."""
    items = ""
    for c in load_contractors():
        items += (
            f'<li class="list-group-item">'
            f'<a href="/contractors/{c.id}/">{c.name}</a> — ИНН {c.inn}'
            f'</li>'
        )
    content = f"""
    <h1>Контрагенты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Контрагенты", content))


def contractor_detail(request, contractor_id):
    """Карточка контрагента."""
    contractors_list = load_contractors()
    contractor = find_contractor_by_id(contractors_list, contractor_id)
    if contractor is None:
        content = """
        <h1 class="text-danger">Контрагент не найден</h1>
        <a href="/contractors/" class="btn btn-outline-secondary">
            ← к списку контрагентов
        </a>
        """
        return HttpResponse(
            page("Контрагент не найден", content), status=404
        )
    content = f"""
    <div class="card">
        <div class="card-body">
            <h1 class="card-title">{contractor.name}</h1>
            <p class="card-text"><strong>ID:</strong> {contractor.id}</p>
            <p class="card-text"><strong>ИНН:</strong> {contractor.inn}</p>
            <a href="/contractors/" class="btn btn-outline-secondary">
                ← к списку контрагентов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(contractor.name, content))
