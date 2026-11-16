from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "contract", "contractor_name", "amount", "payment_date")
    list_filter = ("payment_date",)
    search_fields = ("contract__number", "contract__contractor__name")
    ordering = ("-payment_date", "pk")
    list_select_related = ("contract__contractor",)
    autocomplete_fields = ("contract",)

    @admin.display(description="Контрагент", ordering="contract__contractor__name")
    def contractor_name(self, obj):
        return obj.contract.contractor.name
