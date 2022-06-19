from audioop import reverse
from django.db import transaction

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Account, Assign, AssignDetail 
from .con import ACC_A, ACC_P, ACC_AP
from .utils import assignData, generateLedger, assignData, debitAcc, creditAcc
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
    return assignData(assign_data)

    
@api_view(['POST'])
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
        print(e)
        return Response(e, status=status.HTTP_400_BAD_REQUEST)

    
    return Response(status=status.HTTP_201_CREATED)