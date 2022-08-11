from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (create_subscriber, 
                    TaxView, 
                    subscribe_tax, 
                    assign_tax,
                    init,
                    unpaid,
                    pay)


router = DefaultRouter()
router.register('tax', TaxView)


urlpatterns = [
    path('create_subscriber/', create_subscriber),
    path('subscribe_tax/', subscribe_tax),
    path('assign_tax/', assign_tax),
    path('init/', init),
    path('unpaid/', unpaid),
    path('pay/', pay),
    path('', include(router.urls)),
]