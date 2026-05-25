"""Переименование Resurs → Resource и приведение полей к английскому."""
from django.db import migrations, models


TYPE_MAP = {
    "otkrytoe": "open_seat",
    "fiksirovannyj": "fixed_desk",
    "privatnyj": "private_office",
    "peregovornaya": "meeting_room",
}


def forward_type_values(apps, schema_editor):
    Resource = apps.get_model("resources", "Resource")
    for old, new in TYPE_MAP.items():
        Resource.objects.filter(type=old).update(type=new)


def reverse_type_values(apps, schema_editor):
    Resource = apps.get_model("resources", "Resource")
    for old, new in TYPE_MAP.items():
        Resource.objects.filter(type=new).update(type=old)


class Migration(migrations.Migration):

    dependencies = [
        ("resources", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(old_name="Resurs", new_name="Resource"),
        migrations.RenameField(model_name="resource", old_name="nazvanie", new_name="name"),
        migrations.RenameField(model_name="resource", old_name="tip", new_name="type"),
        migrations.RenameField(model_name="resource", old_name="opisanie", new_name="description"),
        migrations.RenameField(model_name="resource", old_name="vmestimost", new_name="capacity"),
        migrations.RenameField(model_name="resource", old_name="tsena_za_chas", new_name="price_per_hour"),
        migrations.RenameField(model_name="resource", old_name="oborudovanie", new_name="equipment"),
        migrations.RenameField(model_name="resource", old_name="foto", new_name="photo"),
        migrations.RenameField(model_name="resource", old_name="aktiven", new_name="is_active"),
        migrations.RunPython(forward_type_values, reverse_type_values),
        migrations.AlterField(
            model_name="resource",
            name="type",
            field=models.CharField(
                choices=[
                    ("open_seat", "Открытое рабочее место"),
                    ("fixed_desk", "Фиксированный стол"),
                    ("private_office", "Приватный кабинет"),
                    ("meeting_room", "Переговорная комната"),
                ],
                max_length=32,
                verbose_name="Тип ресурса",
            ),
        ),
        migrations.AlterField(
            model_name="resource",
            name="photo",
            field=models.ImageField(
                blank=True, null=True, upload_to="resources/", verbose_name="Фотография"
            ),
        ),
        migrations.RemoveField(model_name="resource", name="data_sozdaniya"),
        migrations.AlterModelOptions(
            name="resource",
            options={
                "ordering": ["type", "name"],
                "verbose_name": "Ресурс",
                "verbose_name_plural": "Ресурсы",
            },
        ),
    ]
