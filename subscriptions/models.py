"""Модели тарифов и абонементов коворкинга."""
from django.conf import settings
from django.db import models
from django.utils import timezone


class Tariff(models.Model):
    """Тариф — общая характеристика абонемента (разовый, дневной, месячный и т.п.)."""

    TYPE_SINGLE = "single"
    TYPE_DAILY = "daily"
    TYPE_MONTHLY = "monthly"
    TYPE_UNLIMITED = "unlimited"
    TYPES = [
        (TYPE_SINGLE, "Разовое посещение"),
        (TYPE_DAILY, "Дневной"),
        (TYPE_MONTHLY, "Месячный"),
        (TYPE_UNLIMITED, "Безлимитный"),
    ]

    name = models.CharField("Название тарифа", max_length=128)
    type = models.CharField("Тип", max_length=16, choices=TYPES)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена, ₽", max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(
        "Срок действия, дней",
        default=1,
        help_text="Сколько дней действует абонемент после покупки",
    )
    hours_per_day = models.PositiveIntegerField(
        "Часов в сутки",
        default=8,
        help_text="Максимум часов бронирования в сутки по этому тарифу",
    )
    is_active = models.BooleanField("Доступен для покупки", default=True)

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        ordering = ["price"]

    def __str__(self) -> str:
        return f"{self.name} ({self.price} ₽)"


class Subscription(models.Model):
    """Приобретённый пользователем абонемент."""

    STATUS_ACTIVE = "active"
    STATUS_EXPIRED = "expired"
    STATUS_CANCELLED = "cancelled"
    STATUSES = [
        (STATUS_ACTIVE, "Активен"),
        (STATUS_EXPIRED, "Истёк"),
        (STATUS_CANCELLED, "Отменён"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.PROTECT,
        related_name="subscriptions",
        verbose_name="Тариф",
    )
    purchase_date = models.DateTimeField("Дата покупки", auto_now_add=True)
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    status = models.CharField(
        "Статус", max_length=16, choices=STATUSES, default=STATUS_ACTIVE
    )

    class Meta:
        verbose_name = "Абонемент"
        verbose_name_plural = "Абонементы"
        ordering = ["-purchase_date"]

    def __str__(self) -> str:
        return f"{self.tariff.name} — {self.user}"

    @property
    def is_current(self) -> bool:
        today = timezone.localdate()
        return (
            self.status == self.STATUS_ACTIVE
            and self.start_date <= today <= self.end_date
        )
