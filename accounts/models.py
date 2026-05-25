"""Модели пользователей коворкинга с поддержкой ролей."""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель пользователя с ролями и профилем."""

    ROLE_GUEST = "guest"
    ROLE_MEMBER = "member"
    ROLE_ADMIN = "admin"
    ROLES = [
        (ROLE_GUEST, "Гость"),
        (ROLE_MEMBER, "Участник"),
        (ROLE_ADMIN, "Администратор"),
    ]

    middle_name = models.CharField("Отчество", max_length=64, blank=True)
    phone = models.CharField("Телефон", max_length=32, blank=True)
    role = models.CharField(
        "Роль",
        max_length=16,
        choices=ROLES,
        default=ROLE_MEMBER,
    )
    avatar = models.ImageField(
        "Аватар", upload_to="avatars/", blank=True, null=True
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        fio = " ".join(filter(None, [self.last_name, self.first_name, self.middle_name]))
        return fio or self.username

    @property
    def full_name(self) -> str:
        return str(self)

    @property
    def is_administrator(self) -> bool:
        return self.role == self.ROLE_ADMIN or self.is_superuser

    @property
    def is_member(self) -> bool:
        return self.role in {self.ROLE_MEMBER, self.ROLE_ADMIN} or self.is_superuser
