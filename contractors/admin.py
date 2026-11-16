from django.contrib import admin

from contracts.models import Contract

from .models import Contractor


class ContractInline(admin.TabularInline):
    model = Contract
    fields = ("number", "amount", "end_date", "is_terminated")
    readonly_fields = fields
    extra = 0
    show_change_link = True

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ("name", "inn")
    search_fields = ("name", "inn")
    ordering = ("name", "pk")
    inlines = (ContractInline,)
