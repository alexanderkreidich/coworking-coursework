"""Представления для статистики и отчётов."""
from datetime import timedelta
from io import BytesIO

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from openpyxl import Workbook

from accounts.permissions import admin_required
from bookings.models import Booking
from resources.models import Resource


@admin_required
def dashboard(request):
    """Главная страница статистики с графиками."""
    today = timezone.localdate()
    days = 30
    start = today - timedelta(days=days - 1)

    bookings = Booking.objects.filter(
        date__gte=start, date__lte=today
    ).exclude(status=Booking.STATUS_CANCELLED)

    # Загруженность по дням
    per_day_qs = (
        bookings.values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )
    by_day = {r["date"]: r["count"] for r in per_day_qs}
    day_labels = []
    day_values = []
    for i in range(days):
        d = start + timedelta(days=i)
        day_labels.append(d.strftime("%d.%m"))
        day_values.append(by_day.get(d, 0))

    # Популярность ресурсов
    popular = list(
        bookings.values("resource__name")
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    # Активность пользователей
    active_users = list(
        bookings.values(
            "user__last_name", "user__first_name", "user__username"
        )
        .annotate(count=Count("id"))
        .order_by("-count")[:10]
    )

    # Сводка
    summary = {
        "total_bookings": bookings.count(),
        "total_resources": Resource.objects.count(),
        "active_resources": Resource.objects.filter(is_active=True).count(),
        "total_hours": sum(
            (b.duration_hours for b in bookings), start=0.0
        ),
    }

    context = {
        "summary": summary,
        "day_labels": day_labels,
        "day_values": day_values,
        "popular": popular,
        "active_users": active_users,
        "days": days,
    }
    return render(request, "stats/dashboard.html", context)


@admin_required
def export_report(request):
    """Экспорт отчёта по бронированиям в формате XLSX."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Бронирования"
    ws.append(
        [
            "ID",
            "Дата",
            "Начало",
            "Окончание",
            "Ресурс",
            "Тип ресурса",
            "Пользователь",
            "Статус",
            "Часов",
            "Стоимость, ₽",
        ]
    )
    qs = (
        Booking.objects.select_related("resource", "user")
        .all()
        .order_by("-date", "-time_start")
    )
    for b in qs:
        ws.append(
            [
                b.id,
                b.date.strftime("%Y-%m-%d"),
                b.time_start.strftime("%H:%M"),
                b.time_end.strftime("%H:%M"),
                b.resource.name,
                b.resource.get_type_display(),
                str(b.user),
                b.get_status_display(),
                b.duration_hours,
                b.cost,
            ]
        )

    for column in ws.columns:
        length = max((len(str(cell.value or "")) for cell in column), default=10)
        ws.column_dimensions[column[0].column_letter].width = min(length + 2, 40)

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="bookings_report.xlsx"'
    return response
