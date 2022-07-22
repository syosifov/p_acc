from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import create_subscriber, TaxView


router = DefaultRouter()
router.register('tax', TaxView)


urlpatterns = [
    path('create_subscriber/', create_subscriber),
    path('', include(router.urls)),
]