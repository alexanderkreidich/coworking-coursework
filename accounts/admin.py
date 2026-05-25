"""Админка пользователей."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "last_name",
        "first_name",
        "email",
        "phone",
        "role",
        "is_active",
    )
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "last_name", "first_name", "email", "phone")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("middle_name", "phone", "role", "avatar")}),
    )
