from importlib.resources import path
from xml.etree.ElementInclude import include
from django.urls import path

from .views import (AccView, db_init, assign_view,
                    reversalView, signUp, logout)
from .login import CustomAuthToken


urlpatterns = [
    path('accounts/', AccView.as_view()),
    path('assign/', assign_view),
    path('init/', db_init),
    path('reverse/', reversalView),
    path('signup/', signUp),
    path('logout/', logout),
    path('login/', CustomAuthToken.as_view()),
]
