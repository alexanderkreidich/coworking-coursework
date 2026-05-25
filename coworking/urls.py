"""Главная маршрутизация проекта коворкинга."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="resources:catalog", permanent=False)),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("resources/", include("resources.urls", namespace="resources")),
    path("bookings/", include("bookings.urls", namespace="bookings")),
    path("subscriptions/", include("subscriptions.urls", namespace="subscriptions")),
    path("stats/", include("stats.urls", namespace="stats")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
