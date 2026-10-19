from django.shortcuts import render

"""Страницы договоров."""

from django.http import HttpResponse

from homepage.views import page
from models.contracts import find_contract_by_id
from storage import load_contracts, load_contractors


def _load_all():
    """Загрузить контрагентов и договоры (связи)."""
    contractors_list = load_contractors()
    contracts_list = load_contracts(contractors_list)
    return contracts_list


def contracts(request):
    """Список договоров."""
    items = ""
    for c in _load_all():
        badge = "bg-danger" if c.status() == "Просрочен" else "bg-success"
        items += (
            f'<li class="list-group-item">'
            f'<a href="/contracts/{c.id}/">№{c.number}</a> — '
            f'{c.contractor.name} — '
            f'{c.total_amount():.2f} руб. — '
            f'<span class="badge {badge}">{c.status()}</span>'
            f'</li>'
        )
    content = f"""
    <h1>Договоры</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Договоры", content))


def contract_detail(request, contract_id):
    """Карточка договора."""
    contracts_list = _load_all()
    contract = find_contract_by_id(contracts_list, contract_id)
    if contract is None:
        content = """
        <h1 class="text-danger">Договор не найден</h1>
        <a href="/contracts/" class="btn btn-outline-secondary">
            ← к списку договоров
        </a>
        """
        return HttpResponse(
            page("Договор не найден", content), status=404
        )
    badge = "bg-danger" if contract.status() == "Просрочен" else "bg-success"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h1 class="card-title">Договор №{contract.number}</h1>
            <p class="card-text"><strong>Контрагент:</strong>
                {contract.contractor.name}</p>
            <p class="card-text"><strong>Период:</strong>
                {contract.start_date} — {contract.end_date}</p>
            <p class="card-text"><strong>Сумма без НДС:</strong>
                {contract.amount:.2f} руб.</p>
            <p class="card-text"><strong>Итого с НДС:</strong>
                {contract.total_amount():.2f} руб.</p>
            <p class="card-text"><strong>Статус:</strong>
                <span class="badge {badge}">{contract.status()}</span></p>
            <a href="/contracts/" class="btn btn-outline-secondary">
                ← к списку договоров
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Договор №{contract.number}", content))
