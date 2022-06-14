from rest_framework.response import Response
from rest_framework import status

from .models import Account 
from .con import ACC_A, ACC_P, ACC_AP
from .serializers import AccountSerializer, AssignSerializer



def debitAcc(name, amount, idAssign):
    acc_debit  = Account.objects.get(pk=name)
    if acc_debit.acc_type == ACC_A or acc_debit.acc_type == ACC_AP:
        newAssets = acc_debit.assets + amount
        newBalance = newAssets - acc_debit.liabilities
        newData = {'assets': newAssets, 'balance': newBalance}
        accSerializer = AccountSerializer(acc_debit, data=newData)
        if accSerializer.is_valid():
            accSerializer.save()
    else: 
        newAssets = acc_debit.assets + amount
        newBalance = acc_debit.liabilities - newAssets
        newData = {'assets': newAssets, 'balance': newBalance}
        accSerializer = AccountSerializer(acc_debit, data=newData)
        if accSerializer.is_valid():
            accSerializer.save()

    if acc_debit.parent != None:
        debitAcc(acc_debit.parent, amount)


def creditAcc(name, amount):
    acc_credit  = Account.objects.get(pk=name)
    if acc_credit.acc_type == ACC_A or acc_credit.acc_type == ACC_AP:
        newLiabilities = acc_credit.liabilities + amount
        newBalance = acc_credit.assets - newLiabilities
        newData = {'liabilities': newLiabilities, 'balance': newBalance}
        accSerializer = AccountSerializer(acc_credit, data=newData)
        if accSerializer.is_valid():
            accSerializer.save()
    else:
        newLiabilities = acc_credit.liabilities + amount
        newBalance = newLiabilities - acc_credit.assets
        newData = {'liabilities': newLiabilities, 'balance': newBalance}
        accSerializer = AccountSerializer(acc_credit, data=newData)
        if accSerializer.is_valid():
            accSerializer.save()
    
    if acc_credit.parent != None:
        creditAcc(acc_credit.parent, amount)


def save_acc(acc):
    serializer = AccountSerializer(data=acc)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return serializer.data
    else:
        raise Exception(serializer.error_messages)


def generateLedger():
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

    for i in range(1,4):
        acc = {}
        acc['name'] = f'411{i:02d}'
        acc['description'] = f'ap. {i:02d}'
        acc['acc_type'] = ACC_A
        acc['parent'] = '411'
        save_acc(acc)

    return Response(status=status.HTTP_201_CREATED)

