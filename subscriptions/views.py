"""Представления для покупки и управления абонементами."""
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Subscription, Tariff


def tariff_list(request):
    """Открытый список тарифов."""
    tariffs = Tariff.objects.filter(is_active=True)
    return render(request, "subscriptions/tariffs.html", {"tariffs": tariffs})


@login_required
def purchase_subscription(request, tariff_pk):
    """Покупка (оформление) абонемента — без реальной оплаты, учебная демонстрация."""
    tariff = get_object_or_404(Tariff, pk=tariff_pk, is_active=True)
    if request.method == "POST":
        today = timezone.localdate()
        Subscription.objects.create(
            user=request.user,
            tariff=tariff,
            start_date=today,
            end_date=today + timedelta(days=tariff.duration_days),
        )
        messages.success(
            request,
            f"Абонемент «{tariff.name}» успешно оформлен.",
        )
        return redirect("accounts:profile")
    return render(request, "subscriptions/confirm.html", {"tariff": tariff})


@login_required
def extend_subscription(request, pk):
    """Продление абонемента — сдвигает дату окончания на срок тарифа."""
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == "POST":
        subscription.end_date = subscription.end_date + timedelta(
            days=subscription.tariff.duration_days
        )
        subscription.status = Subscription.STATUS_ACTIVE
        subscription.save()
        messages.success(request, "Абонемент успешно продлён.")
        return redirect("accounts:profile")
    return render(
        request, "subscriptions/extend.html", {"subscription": subscription}
    )
