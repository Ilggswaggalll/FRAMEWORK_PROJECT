"""Маршруты договоров."""

from django.urls import path

from . import views

app_name = "contracts"

urlpatterns = [
    path("", views.contracts, name="list"),
    path("<int:contract_id>/", views.contract_detail, name="detail"),
    path("overdue/", views.overdue_contracts, name="overdue"),
    path("statistics/", views.statistics, name="statistics"),
]