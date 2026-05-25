# Веб-приложение для управления коворкинг-пространством

Курсовая работа по дисциплине «Разработка веб-приложений».

**Автор:** Крейдич Александр Дмитриевич, группа 241-327
**Направление:** 09.03.01 «Информатика и вычислительная техника»

## Возможности

- Регистрация, вход, восстановление пароля
- Личный кабинет: профиль, история бронирований, абонементы
- Каталог ресурсов (рабочие места, переговорные) с фильтрацией и поиском
- Система бронирования с проверкой конфликтов
- Тарифы и абонементы (разовый, дневной, месячный, безлимитный)
- Панель администратора: CRUD ресурсов, все бронирования
- Статистика: загруженность по дням, популярные ресурсы, активные пользователи
- Экспорт отчётов в XLSX
- Загрузка фотографий ресурсов

## Технологии

- Python 3.12+ / Django 5.1
- PostgreSQL 14+
- Bootstrap 5, Chart.js
- openpyxl, Pillow

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

createdb coworking_db
createuser coworking

python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Открыть: http://127.0.0.1:8000/

## Тестовые учётные записи

| Логин     | Пароль       | Роль          |
|-----------|--------------|---------------|
| admin     | admin12345   | Администратор |
| ivanov    | test12345    | Участник      |
| petrova   | test12345    | Участник      |
| sidorov   | test12345    | Участник      |
| kuznetsova| test12345    | Участник      |

## Переменные окружения

| Переменная   | Значение по умолчанию |
|--------------|-----------------------|
| `DB_NAME`    | coworking_db          |
| `DB_USER`    | coworking             |
| `DB_PASSWORD`| coworking             |
| `DB_HOST`    | localhost             |
| `DB_PORT`    | 5432                  |
| `SECRET_KEY` | (dev-ключ)            |
| `DEBUG`      | 1                     |

## Структура проекта

```
coworking/         — настройки, корневые URL
accounts/          — пользователи, роли, личный кабинет
resources/         — рабочие места и переговорные
bookings/          — бронирования
subscriptions/     — тарифы, абонементы
stats/             — статистика и отчёты
templates/         — HTML-шаблоны
static/            — CSS, изображения
media/             — загружаемые файлы
```

## Развёртывание на хостинге

Минимальный сценарий (Ubuntu + gunicorn + nginx):

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn coworking.wsgi:application --bind 0.0.0.0:8000
```
