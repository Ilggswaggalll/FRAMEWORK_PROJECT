"""Маршруты контрагентов."""

from django.urls import path

from . import views

app_name = "contractors"

urlpatterns = [
    path("", views.contractors, name="list"),
    path("<int:contractor_id>/", views.contractor_detail, name="detail"),
]