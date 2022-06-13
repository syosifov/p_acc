from django.db import transaction

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Account 
from .con import ACC_A, ACC_P, ACC_AP
# import acc.con
from .serializers import AccountSerializer, AssignSerializer


def save_acc(acc):
    serializer = AccountSerializer(data=acc)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return serializer.data
    else:
        raise Exception(serializer.error_messages)


@api_view(['POST'])
@transaction.atomic
def db_init(request):
    print("Load data")

    rout = save_acc({})
    section = {}
    section['parent'] = rout['name']
    sub_section = {}

    with open("notes.txt", "r") as fp:
        for line in fp:
            line = line[:-1]
            sa = line.split(' | ')
            if len(sa[0]) == 1:
                section['name'] = sa[0]
                section['description'] = sa[1]
                section = save_acc(section)
            elif len(sa[0]) == 2:
                sub_section['name'] = sa[0]
                sub_section['description'] = sa[1]
                sub_section['parent'] = section['name']
                sub_section = save_acc(sub_section)
            else:
                acc = {}
                acc['name'] = sa[0]
                acc['description'] = sa[1]
                match sa[2]:
                    case 'Active': acc['acc_type'] = ACC_A
                    case 'Passive': acc['acc_type'] = ACC_P
                    case _: acc['acc_type'] = ACC_AP
                acc['parent'] = sub_section['name']
                save_acc(acc)

    for i in range(3):
        acc = {}
        acc['name'] = f'411{i:02d}'
        acc['description'] = f'ap. {i:02d}'
        acc['acc_type'] = ACC_A
        acc['parent'] = '411'
        save_acc(acc)

    return Response(status=status.HTTP_201_CREATED)


# Create your views here.
class AccView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


@api_view(['POST'])
def assign_view(request):
    
    assign_data = request.data['lstAssgn'][0]
    assign_data['description'] = request.data['description']
    print(assign_data)

    try:
        debit = request.data['lstAssgn'][0]['debit']
        credit = request.data['lstAssgn'][0]['credit']
        amount = request.data['lstAssgn'][0]['amount']
        debitAcc(debit, amount)
        creditAcc(credit, amount)
        serializer = AssignSerializer(data = assign_data)
        if serializer.is_valid():
            serializer.save()
        
    except Exception as e:
        print(e)

    return Response(status=status.HTTP_200_OK)


def debitAcc(name, amount):
    acc_debit  = Account.objects.get(pk=name)
    match acc_debit.acc_type:
        case 0 | 2: 
            newAssets = acc_debit.assets + amount
            newBalance = acc_debit.balance + amount
            newData = {'assets': newAssets, 'balance': newBalance}
            accSerializer = AccountSerializer(acc_debit, data=newData)
            if accSerializer.is_valid():
                accSerializer.save()
        case _: 
            newAssets = acc_debit.assets - amount
            newBalance = acc_debit.balance - amount
            newData = {'assets': newAssets, 'balance': newBalance}
            accSerializer = AccountSerializer(acc_debit, data=newData)
            if accSerializer.is_valid():
                accSerializer.save()
    if acc_debit.parent != None:
        debitAcc(acc_debit.parent, amount)


def creditAcc(name, amount):
    acc_credit  = Account.objects.get(pk=name)
    match acc_credit.acc_type:
        case 0 | 2: 
            newLiabilities = acc_credit.liabilities + amount
            newBalance = acc_credit.assets - newLiabilities
            newData = {'liabilities': newLiabilities, 'balance': newBalance}
            accSerializer = AccountSerializer(acc_credit, data=newData)
            if accSerializer.is_valid():
                accSerializer.save()
        case _: 
            newLiabilities = acc_credit.liabilities + amount
            newBalance = acc_credit.assets + newLiabilities
            newData = {'liabilities': newLiabilities, 'balance': newBalance}
            accSerializer = AccountSerializer(acc_credit, data=newData)
            if accSerializer.is_valid():
                accSerializer.save()
    if acc_credit.parent != None:
        creditAcc(acc_credit.parent, amount)

