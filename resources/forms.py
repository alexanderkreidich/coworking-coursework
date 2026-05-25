"""Формы для работы с ресурсами коворкинга."""
from django import forms

from .models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            "name",
            "type",
            "description",
            "capacity",
            "price_per_hour",
            "equipment",
            "photo",
            "is_active",
        ]


class ResourceFilterForm(forms.Form):
    search = forms.CharField(label="Поиск", required=False, max_length=128)
    type = forms.ChoiceField(
        label="Тип",
        required=False,
        choices=[("", "Все типы")] + list(Resource.TYPES),
    )
    capacity_min = forms.IntegerField(label="Вместимость от", required=False, min_value=1)
    price_max = forms.DecimalField(
        label="Цена до, ₽/час", required=False, max_digits=10, decimal_places=2
    )
