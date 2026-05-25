"""Представления для системы бронирования."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from accounts.permissions import admin_required, member_required
from resources.models import Resource

from .forms import BookingForm
from .models import Booking


@member_required
def create_booking(request, resource_pk=None):
    """Создание нового бронирования."""
    resource = None
    if resource_pk:
        resource = get_object_or_404(Resource, pk=resource_pk, is_active=True)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            try:
                booking.full_clean()
                booking.save()
                messages.success(
                    request, "Бронирование успешно создано."
                )
                return redirect("bookings:my_bookings")
            except ValidationError as error:
                for field, msgs in error.message_dict.items():
                    for msg in msgs:
                        form.add_error(field if field != "__all__" else None, msg)
    else:
        form = BookingForm(initial={"resource": resource} if resource else None)
        if resource:
            form.fields["resource"].initial = resource.pk

    return render(
        request,
        "bookings/form.html",
        {"form": form, "resource": resource},
    )


@login_required
def my_bookings(request):
    """Список бронирований текущего пользователя."""
    bookings = request.user.bookings.select_related("resource").order_by(
        "-date", "-time_start"
    )
    return render(
        request,
        "bookings/my_list.html",
        {"bookings": bookings},
    )


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if (
        booking.user_id != request.user.id
        and not request.user.is_administrator
    ):
        raise PermissionDenied("Вы не можете просматривать чужие бронирования.")
    return render(
        request, "bookings/detail.html", {"booking": booking}
    )


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if (
        booking.user_id != request.user.id
        and not request.user.is_administrator
    ):
        raise PermissionDenied("Вы не можете отменить это бронирование.")
    if request.method == "POST":
        booking.status = Booking.STATUS_CANCELLED
        booking.save()
        messages.success(request, "Бронирование отменено.")
        return redirect("bookings:my_bookings")
    return render(
        request, "bookings/cancel.html", {"booking": booking}
    )


@admin_required
def all_bookings(request):
    bookings = (
        Booking.objects.select_related("resource", "user")
        .all()
        .order_by("-date", "-time_start")
    )
    return render(
        request,
        "bookings/all_bookings.html",
        {"bookings": bookings},
    )
