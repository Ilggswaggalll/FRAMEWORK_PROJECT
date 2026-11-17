"""Маршруты договоров."""

from django.urls import path

from . import views

app_name = "contracts"

urlpatterns = [
    path("new/", views.contract_create, name="create"),
    path("<int:contract_id>/edit/", views.contract_edit, name="edit"),
    path("<int:contract_id>/terminate/", views.contract_terminate, name="terminate"),
    path("", views.contracts, name="list"),
    path("<int:contract_id>/", views.contract_detail, name="detail"),
    path("overdue/", views.overdue_contracts, name="overdue"),
    path("statistics/", views.statistics, name="statistics"),
]
