"""Страницы контрагентов."""

from django.shortcuts import redirect, render

from .models import Contractor


def contractors(request):
    """Список контрагентов."""
    rows = Contractor.objects.order_by("name")
    return render(
        request, "contractors/contractor_list.html", {"contractors": rows}
    )


def contractor_detail(request, contractor_id, slug=None):
    """Карточка контрагента."""
    contractor = Contractor.objects.filter(pk=contractor_id).first()
    if contractor and slug is not None and slug != contractor.slug:
        return redirect(contractor)
    return render(
        request,
        "contractors/contractor_detail.html",
        {"contractor": contractor},
        status=404 if contractor is None else 200,
    )
