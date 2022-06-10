from importlib.resources import path
from xml.etree.ElementInclude import include
from django.urls import path

from .views import AccView, db_init
     

urlpatterns = [
    path('accounts/', AccView.as_view()),
    path('init/', db_init),
]
