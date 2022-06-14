from django.db import transaction

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Account 
from .con import ACC_A, ACC_P, ACC_AP
from .utils import debitAcc, creditAcc, generateLedger
from .serializers import AccountSerializer, AssignSerializer

@api_view(['POST'])
@transaction.atomic
def db_init(request):
    print("Load data")
    response = generateLedger()
    return response

    
# Create your views here.
class AccView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


@api_view(['POST'])
@transaction.atomic
def assign_view(request):
    
    assign_data = request.data['lstAssgn'][0]
    assign_data['description'] = request.data['description']
    print(assign_data)

    try:
        debit = request.data['lstAssgn'][0]['debit']
        credit = request.data['lstAssgn'][0]['credit']
        amount = request.data['lstAssgn'][0]['amount']
        serializer = AssignSerializer(data = assign_data)
        if serializer.is_valid():
            serializer.save()
        idAssign = serializer.data['id']
        debitAcc(debit, amount, idAssign)
        creditAcc(credit, amount, idAssign)
        
    except Exception as e:
        print(e)

    return Response(status=status.HTTP_201_CREATED)


