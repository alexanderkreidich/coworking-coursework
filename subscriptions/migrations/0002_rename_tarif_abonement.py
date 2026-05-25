"""Переименование Tarif → Tariff, Abonement → Subscription и приведение полей к английскому."""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


TARIFF_TYPE_MAP = {
    "razovyj": "single",
    "dnevnoj": "daily",
    "mesyachnyj": "monthly",
    "bezlimitnyj": "unlimited",
}

SUBSCRIPTION_STATUS_MAP = {
    "aktiven": "active",
    "istek": "expired",
    "otmenen": "cancelled",
}


def forward_tariff_type(apps, schema_editor):
    Tariff = apps.get_model("subscriptions", "Tariff")
    for old, new in TARIFF_TYPE_MAP.items():
        Tariff.objects.filter(type=old).update(type=new)


def reverse_tariff_type(apps, schema_editor):
    Tariff = apps.get_model("subscriptions", "Tariff")
    for old, new in TARIFF_TYPE_MAP.items():
        Tariff.objects.filter(type=new).update(type=old)


def forward_subscription_status(apps, schema_editor):
    Subscription = apps.get_model("subscriptions", "Subscription")
    for old, new in SUBSCRIPTION_STATUS_MAP.items():
        Subscription.objects.filter(status=old).update(status=new)


def reverse_subscription_status(apps, schema_editor):
    Subscription = apps.get_model("subscriptions", "Subscription")
    for old, new in SUBSCRIPTION_STATUS_MAP.items():
        Subscription.objects.filter(status=new).update(status=old)


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0001_initial"),
        ("accounts", "0002_rename_polzovatel_to_user"),
    ]

    operations = [
        # --- Тариф ---
        migrations.RenameModel(old_name="Tarif", new_name="Tariff"),
        migrations.RenameField(model_name="tariff", old_name="nazvanie", new_name="name"),
        migrations.RenameField(model_name="tariff", old_name="tip", new_name="type"),
        migrations.RenameField(model_name="tariff", old_name="opisanie", new_name="description"),
        migrations.RenameField(model_name="tariff", old_name="tsena", new_name="price"),
        migrations.RenameField(model_name="tariff", old_name="srok_dnej", new_name="duration_days"),
        migrations.RenameField(model_name="tariff", old_name="chasov_v_sutki", new_name="hours_per_day"),
        migrations.RenameField(model_name="tariff", old_name="aktiven", new_name="is_active"),
        migrations.RunPython(forward_tariff_type, reverse_tariff_type),
        migrations.AlterField(
            model_name="tariff",
            name="type",
            field=models.CharField(
                choices=[
                    ("single", "Разовое посещение"),
                    ("daily", "Дневной"),
                    ("monthly", "Месячный"),
                    ("unlimited", "Безлимитный"),
                ],
                max_length=16,
                verbose_name="Тип",
            ),
        ),
        migrations.AlterModelOptions(
            name="tariff",
            options={
                "ordering": ["price"],
                "verbose_name": "Тариф",
                "verbose_name_plural": "Тарифы",
            },
        ),

        # --- Абонемент ---
        migrations.RenameModel(old_name="Abonement", new_name="Subscription"),
        migrations.RenameField(model_name="subscription", old_name="polzovatel", new_name="user"),
        migrations.RenameField(model_name="subscription", old_name="tarif", new_name="tariff"),
        migrations.RenameField(model_name="subscription", old_name="data_pokupki", new_name="purchase_date"),
        migrations.RenameField(model_name="subscription", old_name="data_nachala", new_name="start_date"),
        migrations.RenameField(model_name="subscription", old_name="data_okonchaniya", new_name="end_date"),
        migrations.RunPython(forward_subscription_status, reverse_subscription_status),
        migrations.AlterField(
            model_name="subscription",
            name="status",
            field=models.CharField(
                choices=[
                    ("active", "Активен"),
                    ("expired", "Истёк"),
                    ("cancelled", "Отменён"),
                ],
                default="active",
                max_length=16,
                verbose_name="Статус",
            ),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="subscriptions",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="tariff",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="subscriptions",
                to="subscriptions.tariff",
                verbose_name="Тариф",
            ),
        ),
        migrations.AlterModelOptions(
            name="subscription",
            options={
                "ordering": ["-purchase_date"],
                "verbose_name": "Абонемент",
                "verbose_name_plural": "Абонементы",
            },
        ),
    ]
