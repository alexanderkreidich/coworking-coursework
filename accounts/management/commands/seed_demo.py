"""Команда для заполнения БД демонстрационными данными."""
from datetime import time, timedelta
from decimal import Decimal
from random import choice, randint

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from bookings.models import Booking
from resources.models import Resource
from subscriptions.models import Subscription, Tariff


class Command(BaseCommand):
    help = "Заполняет базу демонстрационными данными коворкинг-пространства."

    def handle(self, *args, **options):
        User = get_user_model()

        # Администратор
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults=dict(
                email="admin@coworking.ru",
                first_name="Александр",
                last_name="Крейдич",
                middle_name="Дмитриевич",
                phone="+7 (999) 000-00-00",
                role=User.ROLE_ADMIN,
                is_staff=True,
                is_superuser=True,
            ),
        )
        if created:
            admin.set_password("admin12345")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Создан администратор: admin / admin12345"))

        # Участники
        members_data = [
            ("ivanov", "Иван", "Иванов", "Сергеевич"),
            ("petrova", "Мария", "Петрова", "Александровна"),
            ("sidorov", "Алексей", "Сидоров", "Викторович"),
            ("kuznetsova", "Анна", "Кузнецова", "Олеговна"),
        ]
        members = []
        for login, first_name, last_name, middle_name in members_data:
            user, created = User.objects.get_or_create(
                username=login,
                defaults=dict(
                    first_name=first_name,
                    last_name=last_name,
                    middle_name=middle_name,
                    email=f"{login}@example.com",
                    phone=f"+7 (999) 000-{randint(10, 99)}-{randint(10, 99)}",
                    role=User.ROLE_MEMBER,
                ),
            )
            if created:
                user.set_password("test12345")
                user.save()
            members.append(user)

        # Ресурсы
        resources_data = [
            ("Открытая зона №1", Resource.TYPE_OPEN_SEAT, 1, 250,
             "Уютное рабочее место в открытом опенспейсе",
             "Розетка, быстрый Wi-Fi, кофе"),
            ("Открытая зона №2", Resource.TYPE_OPEN_SEAT, 1, 250,
             "Место у окна с видом на город", "Розетка, Wi-Fi"),
            ("Фиксированный стол «Бета»", Resource.TYPE_FIXED_DESK, 1, 400,
             "Закреплённое рабочее место с личным шкафчиком",
             "Монитор 27\", регулируемое кресло, шкафчик"),
            ("Фиксированный стол «Гамма»", Resource.TYPE_FIXED_DESK, 1, 400,
             "Тихий угол вдали от общих зон", "Монитор, шкафчик"),
            ("Кабинет «Минимал»", Resource.TYPE_PRIVATE_OFFICE, 2, 800,
             "Приватный кабинет для двоих",
             "Стол, 2 кресла, монитор, дверь на замок"),
            ("Кабинет «Студия»", Resource.TYPE_PRIVATE_OFFICE, 4, 1500,
             "Большой кабинет для небольшой команды",
             "4 рабочих места, флипчарт, телевизор"),
            ("Переговорная «Meet-6»", Resource.TYPE_MEETING_ROOM, 6, 1000,
             "Переговорная на 6 человек",
             "Проектор, флипчарт, видеосвязь Zoom"),
            ("Переговорная «Board-12»", Resource.TYPE_MEETING_ROOM, 12, 2000,
             "Большая переговорная с овальным столом",
             "Телевизор 75\", камера, профессиональные микрофоны"),
        ]
        resources = []
        for name, type_, cap, price, description, equipment in resources_data:
            r, _ = Resource.objects.get_or_create(
                name=name,
                defaults=dict(
                    type=type_,
                    capacity=cap,
                    price_per_hour=Decimal(price),
                    description=description,
                    equipment=equipment,
                ),
            )
            resources.append(r)

        # Тарифы
        tariffs_data = [
            ("Разовое посещение", Tariff.TYPE_SINGLE, 500, 1, 8,
             "Один день в открытой зоне коворкинга."),
            ("Дневной абонемент", Tariff.TYPE_DAILY, 1500, 7, 10,
             "Неделя неограниченных посещений в дневное время."),
            ("Месячный абонемент", Tariff.TYPE_MONTHLY, 12000, 30, 10,
             "Полный доступ в течение 30 дней."),
            ("Безлимит PRO", Tariff.TYPE_UNLIMITED, 25000, 30, 24,
             "Круглосуточный доступ ко всем зонам."),
        ]
        for name, type_, price, duration, hours, description in tariffs_data:
            Tariff.objects.get_or_create(
                name=name,
                defaults=dict(
                    type=type_,
                    price=Decimal(price),
                    duration_days=duration,
                    hours_per_day=hours,
                    description=description,
                ),
            )

        # Абонементы
        today = timezone.localdate()
        monthly = Tariff.objects.get(name="Месячный абонемент")
        for m in members[:2]:
            Subscription.objects.get_or_create(
                user=m,
                tariff=monthly,
                defaults=dict(
                    start_date=today - timedelta(days=5),
                    end_date=today + timedelta(days=25),
                ),
            )

        # Бронирования за последние 30 дней
        if Booking.objects.count() < 50:
            for _ in range(80):
                user = choice(members)
                resource = choice(resources)
                offset = randint(-25, 5)
                date_b = today + timedelta(days=offset)
                start_hour = randint(8, 17)
                duration = randint(1, 3)
                try:
                    booking = Booking(
                        user=user,
                        resource=resource,
                        date=date_b,
                        time_start=time(start_hour, 0),
                        time_end=time(min(start_hour + duration, 22), 0),
                        status=Booking.STATUS_CONFIRMED
                        if offset >= 0
                        else Booking.STATUS_COMPLETED,
                    )
                    booking.full_clean()
                    booking.save()
                except Exception:
                    continue

        self.stdout.write(self.style.SUCCESS("Демо-данные успешно загружены."))
