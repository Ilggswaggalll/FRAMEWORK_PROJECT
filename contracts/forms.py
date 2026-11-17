"""Параметры поиска и фильтрации договоров."""

from decimal import Decimal

from django import forms
from django.core.files.uploadedfile import UploadedFile

from contractors.models import Contractor

from .models import Contract
from .querysets import ContractStatus

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
    end_before = forms.DateField(
        label="Окончание до", required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    status = forms.ChoiceField(
        label="Статус",
        choices=[("", "Все статусы"), *ContractStatus.choices],
        required=False,
    )
    sort = forms.ChoiceField(
        label="Сортировка",
        choices=[(key, label) for key, (_, label) in SORT_ORDERS.items()],
        required=False,
    )


class PositiveAmountField(forms.DecimalField):
    def __init__(self, **kwargs):
        super().__init__(min_value=Decimal("0.01"), **kwargs)


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ("number", "contractor", "amount", "start_date", "end_date", "image")
        field_classes = {"amount": PositiveAmountField}
        widgets = {
            "start_date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "end_date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }
        help_texts = {"image": "Необязательно. JPG, PNG или WebP до 5 МБ."}
        error_messages = {"number": {"unique": "Договор с таким номером уже существует."}}

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if isinstance(image, UploadedFile):
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Размер изображения должен быть не более 5 МБ.")
            if image.image.format not in {"JPEG", "PNG", "WEBP"}:
                raise forms.ValidationError("Выберите изображение JPG, PNG или WebP.")
        return image

    def clean(self):
        data = super().clean()
        start = data.get("start_date")
        end = data.get("end_date")
        if start and end and end < start:
            self.add_error("end_date", "Дата окончания должна быть не раньше даты начала.")
        return data
