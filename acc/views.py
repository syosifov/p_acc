
from unicodedata import name
from django.db import transaction
from django.db.models.signals import post_save

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Account, Assign, AssignDetail 
from .con import ACC_A, ACC_P, ACC_AP
from .utils import assignData, generateLedger, debitAcc, creditAcc
from .serializers import AccountSerializer
import acc.c

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
def assign_view(request):
    try:
        with transaction.atomic():
            assign_data = request.data
            assignData(assign_data)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_201_CREATED)

    
@api_view(['POST'])     # reverse/
def reversalView(request):
    try:
        idToReverse = request.data['ledgerRecId']
        assignToReverse = Assign.objects.get(pk=idToReverse)
        details = assignToReverse.assigndetail_set.all()
        reverseAssign = Assign(description=f"*** сторно - {assignToReverse.description}",
                               total=-assignToReverse.total,
                               reverse=assignToReverse)
        reverseAssign.save()
        assignToReverse.reversed=True
        assignToReverse.save()
        
        for detail in details:
            print(detail)
            assignDetail = AssignDetail(assign=reverseAssign,
                                        debit_acc=detail.debit_acc,
                                        credit_acc=detail.credit_acc,
                                        amount=-detail.amount)
            assignDetail.save()
            debitAcc(assignDetail.debit_acc, assignDetail.amount, assignDetail.id)
            creditAcc(assignDetail.credit_acc, assignDetail.amount, assignDetail.id)
            
        
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_201_CREATED)



@api_view(['POST'])     # create_group/
def create_group(request):
    a411 = Account.objects.get(pk=acc.c.A411)
    a411001 = Account(name=a411.name+'001',
                      acc_type=a411.acc_type,
                      parent=a411,
                      description='001')
    a411001.save()
    return Response(status=status.HTTP_201_CREATED)


