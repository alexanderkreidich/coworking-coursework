"""Переименование Bronirovanie → Booking и приведение полей к английскому."""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


STATUS_MAP = {
    "ozhidanie": "pending",
    "podtverzhdeno": "confirmed",
    "otmeneno": "cancelled",
    "zaversheno": "completed",
}


def forward_status_values(apps, schema_editor):
    Booking = apps.get_model("bookings", "Booking")
    for old, new in STATUS_MAP.items():
        Booking.objects.filter(status=old).update(status=new)


def reverse_status_values(apps, schema_editor):
    Booking = apps.get_model("bookings", "Booking")
    for old, new in STATUS_MAP.items():
        Booking.objects.filter(status=new).update(status=old)


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0001_initial"),
        ("accounts", "0002_rename_polzovatel_to_user"),
        ("resources", "0002_rename_resurs_to_resource"),
    ]

    operations = [
        migrations.RenameModel(old_name="Bronirovanie", new_name="Booking"),
        migrations.RenameField(model_name="booking", old_name="polzovatel", new_name="user"),
        migrations.RenameField(model_name="booking", old_name="resurs", new_name="resource"),
        migrations.RenameField(model_name="booking", old_name="data", new_name="date"),
        migrations.RenameField(model_name="booking", old_name="vremya_nachala", new_name="time_start"),
        migrations.RenameField(model_name="booking", old_name="vremya_okonchaniya", new_name="time_end"),
        migrations.RenameField(model_name="booking", old_name="kommentarij", new_name="comment"),
        migrations.RunPython(forward_status_values, reverse_status_values),
        migrations.AlterField(
            model_name="booking",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Ожидает подтверждения"),
                    ("confirmed", "Подтверждено"),
                    ("cancelled", "Отменено"),
                    ("completed", "Завершено"),
                ],
                default="confirmed",
                max_length=16,
                verbose_name="Статус",
            ),
        ),
        migrations.AlterField(
            model_name="booking",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="booking",
            name="resource",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookings",
                to="resources.resource",
                verbose_name="Ресурс",
            ),
        ),
        migrations.RemoveField(model_name="booking", name="data_sozdaniya"),
        migrations.AlterModelOptions(
            name="booking",
            options={
                "ordering": ["-date", "-time_start"],
                "verbose_name": "Бронирование",
                "verbose_name_plural": "Бронирования",
            },
        ),
        migrations.RemoveIndex(model_name="booking", name="bookings_br_resurs__dd9f9a_idx"),
        migrations.AddIndex(
            model_name="booking",
            index=models.Index(fields=["resource", "date"], name="bookings_bo_resourc_fb86c1_idx"),
        ),
    ]
