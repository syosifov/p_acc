from django.db import transaction

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Account 
from .con import ACC_A, ACC_P, ACC_AP
from .utils import assignData, generateLedger, assignData
from .serializers import AccountSerializer 

@api_view(['POST'])     #init/
@transaction.atomic
def db_init(request):
    print("Load data")
    response = generateLedger()
    return response

    
# accounts/
class AccView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


@api_view(['POST'])     # assign/
@transaction.atomic
def assign_view(request):
    
    assign_data = request.data
    
    resp = assignData(assign_data)
    return resp
    
