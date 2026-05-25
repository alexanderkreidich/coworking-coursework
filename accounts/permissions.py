"""Декораторы и миксины проверки прав доступа."""
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    """Декоратор: пропускает только администраторов."""

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_administrator:
            raise PermissionDenied("Доступ разрешён только администраторам.")
        return view_func(request, *args, **kwargs)

    return wrapper


def member_required(view_func):
    """Декоратор: пропускает участников и администраторов."""

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_member:
            raise PermissionDenied("Доступ разрешён только зарегистрированным участникам.")
        return view_func(request, *args, **kwargs)

    return wrapper


class AdminRequiredMixin(LoginRequiredMixin):
    """Миксин для class-based view — только администраторы."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if not request.user.is_administrator:
            raise PermissionDenied("Доступ разрешён только администраторам.")
        return super().dispatch(request, *args, **kwargs)
