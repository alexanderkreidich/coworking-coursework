"""Формы бронирования."""
from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["resource", "date", "time_start", "time_end", "comment"]
        widgets = {
            "resource": forms.Select(attrs={"class": "form-select"}),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time_start": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "time_end": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "comment": forms.Textarea(
                attrs={"rows": 3, "class": "form-control", "placeholder": "Дополнительные пожелания (необязательно)"}
            ),
        }

    def __init__(self, *args, resource=None, **kwargs):
        super().__init__(*args, **kwargs)
        if resource is not None:
            self.fields["resource"].initial = resource
            self.fields["resource"].widget = forms.HiddenInput()
