# Система учёта договоров

Учебный проект по дисциплине «Технологии разработки приложений на базе
фреймворков». Развивается поэтапно: консольное приложение на объектной
модели (ПР1–ПР3) дополнено веб-интерфейсом на Django (ПР5), веб-интерфейс
переведён на систему шаблонов Django (ПР6), затем на SQLite (ПР7) и Django ORM (ПР9).

## Назначение

Приложение предназначено для учёта и сопровождения договоров организации:
регистрация нового договора, проверка его срока действия и расчёт стоимости
с учётом налога. Система помогает сотрудникам быстро определять статус
договора и избегать работы с просроченными документами.

## Целевая аудитория

- сотрудники договорного отдела;
- менеджеры, работающие с клиентскими договорами;
- руководители, контролирующие сроки и суммы договоров.

## Предметная область

Договорная деятельность организации: заключение, учёт, продление и
закрытие договоров с контрагентами. Ключевые параметры договора —
номер, контрагент, дата заключения, дата окончания, сумма и статус.

## Используемые технологии

- Python 3;
- Django 5.2 — веб-фреймворк;
- Django Template Language (DTL) — шаблоны;
- HTML5, CSS3, JavaScript;
- Bootstrap 5.3 — базовая вёрстка (подключён через CDN);
- SQLite и Django ORM — хранение данных веб-приложения;
- JSON — хранение данных консольной версии;
- pytest — автоматизированные тесты;
- flake8 — проверка качества кода;
- Git.

## Основные сущности

- `Contractor` — контрагент: `id`, `name`, `inn`;
- `Contract` — договор: `id`, `number`, `contractor`, `amount`,
  `start_date`, `end_date`;
- `Payment` — платёж: `id`, `contract`, `amount`, `payment_date`.

### Взаимодействие объектов

- `Contract` хранит ссылку на объект `Contractor`;
- `Payment` хранит ссылку на объект `Contract`;
- коллекции: `list[Contractor]`, `list[Contract]`, `list[Payment]`.

### Основные методы и функции

- `Contract.total_amount()` — итоговая сумма с НДС (20 %);
- `Contract.status()` — статус по дате окончания
  («Действует», «Истекает сегодня», «Просрочен»);
- `Contract.is_valid()` — проверка корректности данных;
- `add_contractor()`, `add_contract()`, `add_payment()` — добавление объектов;
- `find_contractor_by_id()`, `find_contract_by_id()` — поиск по идентификатору;
- `filter_contracts_by_status()`, `sort_contracts_by_amount()`,
  `get_total_amount()` — выборки и статистика.

## Хранение данных

Веб-версия использует Django ORM и базу `db.sqlite3`. Структуру таблиц
задают модели в `contractors/models.py`, `contracts/models.py` и `payments/models.py`
и миграции этих приложений. Договор ссылается на контрагента, платёж — на договор.
Django защищает связанные записи от удаления через `on_delete=PROTECT`.

`data/contracts.sqlite` — исходная база ПР7. Команда `import_legacy_data`
читает её и сохраняет через ORM исходные ID и внешние ключи. Повторный запуск
пропускает совпадающие записи. Консольная версия (`main.py`) использует JSON
через `storage.py`.

## Запуск веб-версии

Из каталога проекта на macOS или Linux выполните:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py import_legacy_data
python manage.py runserver
```

Откройте <http://127.0.0.1:8000/>. Если окружение уже создано и зависимости
установлены, пропустите создание окружения и установку. Сервер останавливается
через Ctrl+C. Для входа в `/admin/` создайте локальную учётную запись командой
`python manage.py createsuperuser`. В админке можно создавать, изменять и удалять записи.

### Проверки

```bash
python manage.py check
python manage.py showmigrations
python manage.py makemigrations --check --dry-run
python -m pytest -v
python -m flake8 . --extend-exclude=venv
```

## Веб-интерфейс (Django)

Список договоров поддерживает поиск по номеру и контрагенту, фильтры по
контрагенту и статусу, сортировку и пагинацию. Представления передают результаты
запросов в шаблоны. Для получения связанных записей используется
`select_related()`, для статистики — `Count`, `Sum`, `annotate()` и
`aggregate()`.

### Django-проект

- пакет конфигурации — `contractly/`;
- точка входа — `manage.py`;
- зарегистрированные приложения: `homepage`, `contractors`, `contracts`,
  `payments`.

### Страницы и URL

| URL | View-функция | Назначение |
|---|---|---|
| `/` | `homepage.views.index` | главная страница, переходы к разделам |
| `/contractors/` | `contractors.views.contractors` | список контрагентов |
| `/contractors/<int:contractor_id>/` | `contractors.views.contractor_detail` | карточка контрагента, при отсутствии — 404 |
| `/contracts/` | `contracts.views.contracts` | список договоров со статусами |
| `/contracts/<int:contract_id>/` | `contracts.views.contract_detail` | карточка договора, при отсутствии — 404 |
| `/contracts/overdue/` | `contracts.views.overdue_contracts` | просроченные договоры |
| `/contracts/statistics/` | `contracts.views.statistics` | статистика по контрагентам |
| `/payments/` | `payments.views.payments` | список платежей |
| `/nonexistent/` | `homepage.views.page_not_found` | собственная страница 404 |

### Маршрутизация

Маршрутизация двухуровневая: корневой `contractly/urls.py` подключает
маршруты приложений через `include()`, в каждом приложении — свой
`urls.py` с `app_name` и именованными маршрутами. Для динамических
адресов используется конвертер `<int:...>`. Обработчик 404 объявлен
в корневом `urls.py` (`handler404`).

В шаблонах ссылки формируются через `{% url %}`, а не через жёстко
прописанные адреса:

```django
{% url 'contractors:list' %}
{% url 'contracts:detail' contract.id %}
```

### Шаблоны Django
Общая структура страниц вынесена в базовый шаблон templates/base.html:
кодировка, <title>, подключение Bootstrap, собственных CSS и JavaScript,
навигация, блоки для заголовка и содержимого.

Дочерние шаблоны подключают базовый через {% extends "base.html" %} и
переопределяют блоки {% block title %} и {% block content %}.

Повторяющиеся фрагменты вынесены в отдельные шаблоны и подключаются через
{% include %}:

templates/includes/navigation.html — общая навигация;

contractors/templates/contractors/includes/contractor_card.html —
карточка контрагента;

contracts/templates/contracts/includes/contract_status.html —
статус договора.

Данные передаются из view в шаблон через словарь контекста:
context = {"contracts": contracts_list}
return render(request, "contracts/contract_list.html", context)


## Структура проекта

```text
PROJECT/
├── .gitignore
├── README.md
├── requirements.txt
├── manage.py
├── main.py
├── storage.py
├── utils.py
├── contractly/                       # пакет конфигурации Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── templates/                        # общие шаблоны проекта
│   ├── base.html
│   └── includes/
│       └── navigation.html
├── homepage/                         # Django-приложение
│   ├── templates/homepage/
│   │   ├── index.html
│   │   └── 404.html
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.png
│   ├── migrations/
│   ├── urls.py
│   ├── views.py
│   └── ...
├── contractors/                      # Django-приложение
│   ├── templates/contractors/
│   │   ├── contractor_list.html
│   │   ├── contractor_detail.html
│   │   └── includes/
│   │       └── contractor_card.html
│   ├── migrations/
│   ├── urls.py
│   ├── views.py
│   └── ...
├── contracts/                        # Django-приложение
│   ├── templates/contracts/
│   │   ├── contract_list.html
│   │   ├── contract_detail.html
│   │   └── includes/
│   │       └── contract_status.html
│   ├── migrations/
│   ├── urls.py
│   ├── views.py
│   └── ...
├── payments/                         # Django-приложение
│   ├── templates/payments/
│   │   └── payment_list.html
│   ├── migrations/
│   ├── urls.py
│   ├── views.py
│   └── ...
├── models/                           # предметная модель (ПР3)
│   ├── __init__.py
│   ├── contractors.py
│   ├── contracts.py
│   └── payments.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── db/
│   ├── __init__.py
│   ├── database.py
│   └── import_json.py
├── data/
│   ├── contracts.sqlite  <-- добавили
│   ├── contractors.json
├── data/
│   ├── contractors.json
│   ├── contracts.json
│   └── payments.json
└── tests/
    ├── test_contractors.py
    ├── test_contracts.py
    └── test_payments.py
```
