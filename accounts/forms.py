"""Формы для работы с пользователями."""
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label="Имя", max_length=64, required=True)
    last_name = forms.CharField(label="Фамилия", max_length=64, required=True)
    middle_name = forms.CharField(label="Отчество", max_length=64, required=False)
    phone = forms.CharField(label="Телефон", max_length=32, required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "last_name",
            "first_name",
            "middle_name",
            "email",
            "phone",
            "password1",
            "password2",
        )


class ProfileForm(forms.ModelForm):
    """Форма редактирования профиля."""

    class Meta:
        model = User
        fields = (
            "last_name",
            "first_name",
            "middle_name",
            "email",
            "phone",
            "avatar",
        )
