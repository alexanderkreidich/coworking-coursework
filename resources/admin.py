"""Админка для ресурсов коворкинга."""
from django.contrib import admin

from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "capacity", "price_per_hour", "is_active")
    list_filter = ("type", "is_active")
    search_fields = ("name", "description", "equipment")
    list_editable = ("is_active",)
