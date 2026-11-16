"""Страницы контрагентов."""

from django.shortcuts import render

from .models import Contractor


def contractors(request):
    """Список контрагентов."""
    rows = Contractor.objects.order_by("name")
    return render(
        request, "contractors/contractor_list.html", {"contractors": rows}
    )


def contractor_detail(request, contractor_id):
    """Карточка контрагента."""
    contractor = Contractor.objects.filter(pk=contractor_id).first()
    return render(
        request,
        "contractors/contractor_detail.html",
        {"contractor": contractor},
        status=404 if contractor is None else 200,
    )
