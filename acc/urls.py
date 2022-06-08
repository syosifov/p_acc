from importlib.resources import path
from xml.etree.ElementInclude import include
from django.urls import path

from .views import AccView
     

urlpatterns = [
    path('accounts/', AccView.as_view())
]
