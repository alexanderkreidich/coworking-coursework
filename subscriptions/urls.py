"""URL-маршруты для абонементов."""
from django.urls import path

from . import views

app_name = "subscriptions"

urlpatterns = [
    path("", views.tariff_list, name="tariffs"),
    path("purchase/<int:tariff_pk>/", views.purchase_subscription, name="purchase"),
    path("extend/<int:pk>/", views.extend_subscription, name="extend"),
]
