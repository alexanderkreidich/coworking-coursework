"""Представления для регистрации, входа и личного кабинета."""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import ProfileForm, RegistrationForm


def register(request):
    """Регистрация нового пользователя."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно. Добро пожаловать!")
            return redirect("accounts:profile")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


class SignInView(LoginView):
    template_name = "accounts/login.html"


class SignOutView(LogoutView):
    next_page = "resources:catalog"


class RequestPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("accounts:login")


@login_required
def profile(request):
    """Главная страница личного кабинета."""
    today = timezone.localdate()
    bookings = request.user.bookings.select_related("resource").order_by(
        "-date", "-time_start"
    )[:10]
    subscriptions = request.user.subscriptions.select_related("tariff").order_by(
        "-purchase_date"
    )
    active_subscription = subscriptions.filter(
        status="active",
        start_date__lte=today,
        end_date__gte=today,
    ).first()
    context = {
        "bookings": bookings,
        "subscriptions": subscriptions,
        "active_subscription": active_subscription,
    }
    return render(request, "accounts/profile.html", context)


@login_required
def edit_profile(request):
    """Редактирование данных профиля."""
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлён.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/edit_profile.html", {"form": form})
