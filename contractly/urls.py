"""Корневая маршрутизация проекта."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("contractors/", include("contractors.urls")),
    path("contracts/", include("contracts.urls")),
    path("payments/", include("payments.urls")),
]

handler404 = "homepage.views.page_not_found"