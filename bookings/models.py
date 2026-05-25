"""Модели бронирования ресурсов коворкинга."""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from resources.models import Resource


class Booking(models.Model):
    """Бронирование ресурса на определённый временной интервал."""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"
    STATUSES = [
        (STATUS_PENDING, "Ожидает подтверждения"),
        (STATUS_CONFIRMED, "Подтверждено"),
        (STATUS_CANCELLED, "Отменено"),
        (STATUS_COMPLETED, "Завершено"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Пользователь",
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Ресурс",
    )
    date = models.DateField("Дата")
    time_start = models.TimeField("Время начала")
    time_end = models.TimeField("Время окончания")
    comment = models.TextField("Комментарий", blank=True)
    status = models.CharField(
        "Статус", max_length=16, choices=STATUSES, default=STATUS_CONFIRMED
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-date", "-time_start"]
        indexes = [
            models.Index(fields=["resource", "date"]),
        ]

    def __str__(self) -> str:
        return f"{self.resource.name} — {self.date} {self.time_start}–{self.time_end}"

    def get_absolute_url(self) -> str:
        return reverse("bookings:detail", args=[self.pk])

    def clean(self) -> None:
        """Проверка корректности: время, пересечения с другими бронированиями."""
        super().clean()
        if self.time_start >= self.time_end:
            raise ValidationError(
                "Время окончания должно быть больше времени начала."
            )

        if self.resource_id and self.date and self.time_start and self.time_end:
            conflicts = (
                Booking.objects.filter(
                    resource=self.resource,
                    date=self.date,
                    status__in=[
                        self.STATUS_PENDING,
                        self.STATUS_CONFIRMED,
                    ],
                    time_start__lt=self.time_end,
                    time_end__gt=self.time_start,
                )
                .exclude(pk=self.pk)
            )
            if conflicts.exists():
                raise ValidationError(
                    "Выбранный интервал пересекается с уже существующим бронированием."
                )

    @property
    def duration_hours(self) -> float:
        start = self.time_start.hour + self.time_start.minute / 60
        end = self.time_end.hour + self.time_end.minute / 60
        return round(end - start, 2)

    @property
    def cost(self) -> float:
        return float(self.resource.price_per_hour) * self.duration_hours
