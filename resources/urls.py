"""URL-маршруты ресурсов коворкинга."""
from django.urls import path

from . import views

app_name = "resources"

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("manage/", views.admin_list, name="admin_list"),
    path("manage/create/", views.create, name="create"),
    path("manage/<int:pk>/edit/", views.edit, name="edit"),
    path("manage/<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/", views.detail, name="detail"),
]
