from .models import Account
from .serializers import AccountSerializer

from rest_framework import generics

# Create your views here.
class AccView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

