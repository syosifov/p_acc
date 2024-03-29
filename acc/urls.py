from django.urls import path

from .views import (AccView, db_init, assign_view,
                    reversalView, create_group)
from .authentication import CustomAuthToken, signUp, logout


urlpatterns = [
    path('accounts/', AccView.as_view()),
    path('assign/', assign_view),
    path('init/', db_init),
    path('reverse/', reversalView),
    path('signup/', signUp),
    path('logout/', logout),
    path('login/', CustomAuthToken.as_view()),
    path('create_group/', create_group),
]
