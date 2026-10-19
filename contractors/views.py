"""Страницы контрагентов."""

from django.shortcuts import render

from models.contractors import find_contractor_by_id
from storage import load_contractors


def contractors(request):
    """Список контрагентов."""
    contractors_list = load_contractors()
    context = {"contractors": contractors_list}
    return render(request, "contractors/contractor_list.html", context)


def contractor_detail(request, contractor_id):
    """Карточка контрагента."""
    contractors_list = load_contractors()
    contractor = find_contractor_by_id(contractors_list, contractor_id)
    context = {"contractor": contractor}
    return render(
        request,
        "contractors/contractor_detail.html",
        context,
        status=404 if contractor is None else 200,
    )