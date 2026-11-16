"""Корневая маршрутизация проекта."""

from django.conf import settings
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

if settings.DEBUG_TOOLBAR_ENABLED:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()
