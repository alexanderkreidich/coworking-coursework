"""Модели ресурсов коворкинга: рабочие места и переговорные комнаты."""
from django.db import models
from django.urls import reverse


class Resource(models.Model):
    """Ресурс коворкинг-пространства — рабочее место или переговорная."""

    TYPE_OPEN_SEAT = "open_seat"
    TYPE_FIXED_DESK = "fixed_desk"
    TYPE_PRIVATE_OFFICE = "private_office"
    TYPE_MEETING_ROOM = "meeting_room"
    TYPES = [
        (TYPE_OPEN_SEAT, "Открытое рабочее место"),
        (TYPE_FIXED_DESK, "Фиксированный стол"),
        (TYPE_PRIVATE_OFFICE, "Приватный кабинет"),
        (TYPE_MEETING_ROOM, "Переговорная комната"),
    ]

    name = models.CharField("Название", max_length=128)
    type = models.CharField("Тип ресурса", max_length=32, choices=TYPES)
    description = models.TextField("Описание", blank=True)
    capacity = models.PositiveIntegerField("Вместимость (чел.)", default=1)
    price_per_hour = models.DecimalField(
        "Цена за час, ₽", max_digits=10, decimal_places=2, default=0
    )
    equipment = models.CharField(
        "Оборудование",
        max_length=255,
        blank=True,
        help_text="Перечислите через запятую: проектор, флипчарт, монитор и т.д.",
    )
    photo = models.ImageField(
        "Фотография", upload_to="resources/", blank=True, null=True
    )
    is_active = models.BooleanField("Доступен для бронирования", default=True)

    class Meta:
        verbose_name = "Ресурс"
        verbose_name_plural = "Ресурсы"
        ordering = ["type", "name"]

    def __str__(self) -> str:
        return f"{self.get_type_display()} — {self.name}"

    def get_absolute_url(self) -> str:
        return reverse("resources:detail", args=[self.pk])

    @property
    def is_meeting_room(self) -> bool:
        return self.type == self.TYPE_MEETING_ROOM
