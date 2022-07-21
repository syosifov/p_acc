from django.urls import path

from .views import create_subscriber


urlpatterns = [
    path('create_subscriber/', create_subscriber),
]