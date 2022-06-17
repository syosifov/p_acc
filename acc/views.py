from django.db import transaction

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Account 
from .con import ACC_A, ACC_P, ACC_AP
from .utils import debitAcc, creditAcc, generateLedger
from .serializers import AccountSerializer, AssignSerializer, AssignDetailSerializer

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
    
    assign_data = request.data
    lstAssign = request.data['lstAssgn']
    
    print(assign_data)
    print(lstAssign)

    try:
        
        a_serializer = AssignSerializer(data = assign_data)
        if a_serializer.is_valid():
            a_serializer.save()
        assign_id = a_serializer.data['id']
        for assign_detail in lstAssign:
            assign_detail['assign'] = assign_id
            ad_serializer = AssignDetailSerializer(data=assign_detail)
            v = ad_serializer.run_validation(data=assign_detail)
            if ad_serializer.is_valid():
                ad_serializer.save()
                id_assign_detail = ad_serializer.data['id']
                debit_acc = assign_detail['debit_acc']
                credit_acc = assign_detail['credit_acc']
                amount = assign_detail['amount']
                debitAcc(debit_acc, amount, id_assign_detail)
                creditAcc(credit_acc, amount)
        
    except Exception as e:
        print(e)
        return Response(e, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)


