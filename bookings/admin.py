"""Админка бронирований."""
from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "resource",
        "user",
        "date",
        "time_start",
        "time_end",
        "status",
    )
    list_filter = ("status", "date", "resource__type")
    search_fields = ("resource__name", "user__username", "user__last_name")
    date_hierarchy = "date"
    list_editable = ("status",)
