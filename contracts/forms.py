"""Параметры поиска и фильтрации договоров."""

from django import forms

from contractors.models import Contractor

SORT_ORDERS = {
    "number": ("number", "По номеру"),
    "end_date": ("end_date", "По ближайшей дате окончания"),
    "amount_desc": ("-amount", "Сначала дороже"),
    "amount_asc": ("amount", "Сначала дешевле"),
}


class ContractFilterForm(forms.Form):
    q = forms.CharField(label="Номер или контрагент", max_length=100, required=False)
    search_scope = forms.ChoiceField(
        label="Где искать",
        choices=[("", "Номер и контрагент"), ("number", "Только номер")],
        required=False,
    )
    contractor = forms.ModelChoiceField(
        label="Контрагент",
        queryset=Contractor.objects.order_by("name", "pk"),
        empty_label="Все контрагенты",
        required=False,
    )
    status = forms.ChoiceField(
        label="Статус",
        choices=[
            ("", "Все статусы"),
            ("active", "Действует"),
            ("today", "Истекает сегодня"),
            ("overdue", "Просрочен"),
        ],
        required=False,
    )
    sort = forms.ChoiceField(
        label="Сортировка",
        choices=[(key, label) for key, (_, label) in SORT_ORDERS.items()],
        required=False,
    )
