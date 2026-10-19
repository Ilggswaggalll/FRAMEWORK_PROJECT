from django.shortcuts import render

"""Главная страница и общий каркас HTML-страниц."""

from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Собрать HTML-документ из заголовка и содержимого."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/contractors/">Контрагенты</a>
        <a class="nav-link" href="/contracts/">Договоры</a>
        <a class="nav-link" href="/payments/">Платежи</a>
    </nav>
    <main class="container mt-3">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница."""
    content = """
    <h1 class="display-4">Система учёта договоров</h1>
    <p class="lead">Учёт договоров, контрагентов и платежей.</p>
    <a href="/contractors/" class="btn btn-primary me-2">Контрагенты</a>
    <a href="/contracts/" class="btn btn-secondary me-2">Договоры</a>
    <a href="/payments/" class="btn btn-outline-secondary">Платежи</a>
    """
    return HttpResponse(page("Система учёта договоров", content))


def page_not_found(request, exception):
    """Страница 404."""
    content = """
    <h1 class="text-danger">404 — страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(page("404", content), status=404)
