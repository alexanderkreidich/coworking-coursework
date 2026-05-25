"""Финальное приведение модели User к английскому именованию.

Старое имя модели (Polzovatel) в БД хранилось как таблица `accounts_polzovatel`.
В миграции 0001 модель уже создаётся под именем `User`, но таблица оставлена
прежней через db_table — это обеспечивает корректную работу ленивых ссылок
AUTH_USER_MODEL = 'accounts.User'. В этой миграции:
  • переименовываем поля (otchestvo → middle_name и т.д.);
  • переводим хранимые значения роли с транслита на английский;
  • убираем избыточное поле data_registratsii (есть date_joined из AbstractUser);
  • переименовываем таблицу в `accounts_user`.
"""
from django.db import migrations, models


def forward_role_values(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.filter(role="gost").update(role="guest")
    User.objects.filter(role="uchastnik").update(role="member")
    User.objects.filter(role="administrator").update(role="admin")


def reverse_role_values(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.filter(role="guest").update(role="gost")
    User.objects.filter(role="member").update(role="uchastnik")
    User.objects.filter(role="admin").update(role="administrator")


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(model_name="user", old_name="otchestvo", new_name="middle_name"),
        migrations.RenameField(model_name="user", old_name="telefon", new_name="phone"),
        migrations.RenameField(model_name="user", old_name="rol", new_name="role"),
        migrations.RunPython(forward_role_values, reverse_role_values),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("guest", "Гость"),
                    ("member", "Участник"),
                    ("admin", "Администратор"),
                ],
                default="member",
                max_length=16,
                verbose_name="Роль",
            ),
        ),
        migrations.RemoveField(model_name="user", name="data_registratsii"),
        migrations.AlterModelTable(name="user", table=None),
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ["-date_joined"],
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
    ]
