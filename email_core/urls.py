from django.urls import path

from .views import send, getUsers, getLocations

urlpatterns = [
    path('email', send),
    path('users', getUsers),
    path('locations', getLocations),
]