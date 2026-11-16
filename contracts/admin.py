from django.contrib import admin

from payments.models import Payment

from .models import Contract
from .querysets import ContractStatus


class ContractStatusFilter(admin.SimpleListFilter):
    title = "статус"
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return ContractStatus.choices

    def queryset(self, request, queryset):
        if self.value() in ContractStatus.values:
            return queryset.with_status(self.value())
        return queryset


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    show_change_link = True


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("number", "contractor", "amount", "end_date", "status_label")
    list_filter = (ContractStatusFilter, "contractor", "end_date")
    search_fields = ("number", "contractor__name", "contractor__inn")
    ordering = ("-end_date", "number")
    list_select_related = ("contractor",)
    autocomplete_fields = ("contractor",)
    inlines = (PaymentInline,)

    @admin.display(description="Статус")
    def status_label(self, obj):
        return obj.status
