"""URL-маршруты бронирования."""
from django.urls import path

from . import views

app_name = "bookings"

urlpatterns = [
    path("my/", views.my_bookings, name="my_bookings"),
    path("all/", views.all_bookings, name="all_bookings"),
    path("create/", views.create_booking, name="create"),
    path("create/<int:resource_pk>/", views.create_booking, name="create_for_resource"),
    path("<int:pk>/", views.booking_detail, name="detail"),
    path("<int:pk>/cancel/", views.cancel_booking, name="cancel"),
]
