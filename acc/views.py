
from django.db import transaction

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Account, Assign, AssignDetail 
from .con import ACC_A, ACC_P, ACC_AP
from .utils import assignData, generateLedger, debitAcc, creditAcc
from .serializers import AccountSerializer, UserSerializer

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
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])         # signup/
@permission_classes([AllowAny])
def signUp(request):
    try:
        with transaction.atomic():
            user = User()
            user.set_password(request.data['password'])
            user.username = request.data['username']
            user.save()
            # token = Token.objects.get(user_id=user.id)
            user_serializer = UserSerializer(user)
            data = user_serializer.data
            # data['token'] = token.key
    except Exception as e:
        return Response(str(e),status=status.HTTP_400_BAD_REQUEST) 
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def logout(request):

    user = request.user
    token = Token.objects.get(user=user)
    token.delete()
    return Response(status=status.HTTP_200_OK)

