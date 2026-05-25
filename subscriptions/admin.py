"""Админка тарифов и абонементов."""
from django.contrib import admin

from .models import Subscription, Tariff


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price", "duration_days", "hours_per_day", "is_active")
    list_filter = ("type", "is_active")
    list_editable = ("is_active",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "tariff", "start_date", "end_date", "status")
    list_filter = ("status", "tariff__type")
    search_fields = ("user__username", "user__last_name")
    date_hierarchy = "purchase_date"
