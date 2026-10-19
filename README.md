# Система учёта договоров

Учебный проект по дисциплине «Технологии разработки приложений на базе
фреймворков». Развивается поэтапно: консольное приложение на объектной
модели (ПР1–ПР3) дополнено веб-интерфейсом на Django (ПР5), веб-интерфейс
переведён на систему шаблонов Django (ПР6).

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
- JSON — хранение данных (Django ORM пока не используется);
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

На текущем этапе данные хранятся в JSON-файлах в каталоге `data/`:

- `data/contractors.json` — контрагенты;
- `data/contracts.json` — договоры;
- `data/payments.json` — платежи.

Загрузка и сохранение выполняются модулем `storage.py`. При загрузке из
JSON создаются объекты предметной области, при сохранении — объекты
преобразуются обратно в словари. Для связанных объектов в JSON хранятся
их идентификаторы (`contractor_id`, `contract_id`).

Django ORM и база данных на данном этапе не используются.

## Веб-интерфейс (Django)

Веб-часть реализована на Django 5.2 и использует существующую предметную
модель ПР3: view-функции вызывают функции из `storage.py` и `models/`,
а не дублируют логику.

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

Шаблоны Django
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

В шаблонах используются:

вывод значений — {{ variable }} и обращение к атрибутам объекта
через точку: {{ contract.contractor.name }};

циклы — {% for contract in contracts %} с блоком {% empty %};

условия — {% if contract %} / {% elif %} / {% else %};

именованные URL — {% url %};

фильтры шаблонов.

Фильтры шаблонов
В проекте используются стандартные фильтры DTL:

{{ contractors|length }} — количество элементов списка;

{{ contractor.name|default:"Без названия" }} — значение по умолчанию,
если поле пустое или отсутствует;

{{ contract.total_amount|floatformat:2 }} — число с двумя знаками
после запятой.

Фильтры применяются для представления данных и не содержат
бизнес-логики приложения.


Статические файлы
Статические файлы приложения homepage расположены в каталоге
homepage/static/homepage/:

homepage/static/homepage/css/style.css — собственные стили проекта;

homepage/static/homepage/js/main.js — автоматическая подстановка
текущего года в подвал страницы;

homepage/static/homepage/img/logo.png — изображение логотипа.

В base.html статические файлы подключаются через {% load static %}
и {% static %}:
{% load static %}
<link rel="stylesheet" href="{% static 'homepage/css/style.css' %}">

Обработка ошибки 404
Для отсутствующих объектов (контрагент или договор с несуществующим
идентификатором) view-функция возвращает render(...) со статусом
status=404 и передаёт в шаблон значение None — шаблон показывает
ветку {% else %} с сообщением «не найден».

Для отсутствующих маршрутов используется handler404,
объявленный в contractly/urls.py и указывающий на
homepage.views.page_not_found, который рендерит
homepage/templates/homepage/404.html.

Формирование HTML-строк в Python-коде view-функций больше не используется:
все страницы формируются шаблонами Django.

Структура проекта
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
├── data/
│   ├── contractors.json
│   ├── contracts.json
│   └── payments.json
└── tests/
    ├── test_contractors.py
    ├── test_contracts.py
    └── test_payments.py



Запуск
Веб-версия (Django)
bash
python manage.py runserver
После запуска открыть в браузере: http://127.0.0.1:8000/

Консольная версия (сохранена с ПР3)
bash
python main.py
Тесты
bash
pytest -v
Автоматизированные тесты ПР3 проверяют работу классов Contractor,
Contract, Payment и функций обработки коллекций; после ПР5 и ПР6
они остаются актуальными и проходят без изменений.

Проверка проекта
bash
python manage.py check
Проверка кода
bash
flake8 . --extend-exclude=venv,*/migrations
Каталоги migrations/ исключены из проверки, поскольку файлы в них
генерируются Django автоматически.

Git
Проект развивается в Git-репозитории. Коммиты, относящиеся к отдельным
практическим работам, помечаются префиксом:

PR3: — объектная модель;

PR5: — Django-проект и веб-страницы;

PR6: — шаблоны Django и статические файлы.

Текущее состояние и план развития
Реализовано (ПР1–ПР6):

объектная модель Contractor, Contract, Payment;

JSON-хранилище;

консольное приложение с меню;

автоматизированные тесты pytest;

Django-проект contractly и четыре приложения;

двухуровневая маршрутизация URL;

view-функции и страницы предметной области;

динамические URL с конвертером <int:...>;

обработка ошибки 404 (своя страница);

базовый шаблон base.html и наследование шаблонов;

включаемые шаблоны ({% include %});

передача данных через контекст;

циклы {% for %} и условия {% if %};

именованные URL и пространства имён в шаблонах;

фильтры шаблонов (length, default, floatformat);

статические файлы (CSS, JavaScript, изображение);

собственное оформление интерфейса поверх Bootstrap.