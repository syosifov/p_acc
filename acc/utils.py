from rest_framework.response import Response
from rest_framework import status

from .models import Account
from .con import ACC_A, ACC_P, ACC_AP, LZ
from .serializers import (AccountSerializer, 
                          AssignSerializer, 
                          AccountHistorySerializer, 
                          AssignDetailSerializer)



def prepareAccHistory(account: Account,
                      id_assign_detail: int,
                      amaount_debit: float = 0,
                      amount_credit: float = 0,
                    ):
    acc_history = {}
    acc_history['name'] = account.name
    acc_history['assignDetail'] = id_assign_detail
    acc_history['assets'] = account.assets
    acc_history['end_assets'] = account.assets
    acc_history['liabilities'] = account.liabilities
    acc_history['end_liablities'] = account.liabilities
    acc_history['amaount_debit'] = amaount_debit
    acc_history['amount_credit'] = amount_credit
    acc_history['balance'] = account.balance
    
    return acc_history


def debitAcc(name, amount, id_assign_detail):

    acc_debit = Account.objects.get(pk=name)
    acc_history = prepareAccHistory(acc_debit,
                                    id_assign_detail,
                                    amaount_debit=amount)
    
    if acc_debit.acc_type == ACC_A or \
       acc_debit.acc_type == ACC_AP:

        newAssets = acc_debit.assets + amount
        newBalance = newAssets - acc_debit.liabilities
        newData = {'assets': newAssets, 'balance': newBalance}
        
        acc_history['end_assets'] = newAssets
        acc_history['end_balance'] = newBalance

        accSerializer = AccountSerializer(acc_debit, data=newData)
        if accSerializer.is_valid():
            accSerializer.save()
    else:
        newAssets = acc_debit.assets + amount
        newBalance = acc_debit.liabilities - newAssets
        newData = {'assets': newAssets, 'balance': newBalance}
        
        acc_history['end_assets'] = newAssets
        acc_history['end_balance'] = newBalance

        accSerializer = AccountSerializer(acc_debit, data=newData)
        if accSerializer.is_valid():
            accSerializer.save()

    accountHistorySerializer = AccountHistorySerializer(data=acc_history)
    accountHistorySerializer.run_validation(data=acc_history)
    if accountHistorySerializer.is_valid():
        accountHistorySerializer.save()

    if acc_debit.parent != None:
        debitAcc(acc_debit.parent, amount, id_assign_detail)


def creditAcc(name, amount, id_assign_detail):
    acc_credit = Account.objects.get(pk=name)
    acc_history = prepareAccHistory(acc_credit,
                                    id_assign_detail,
                                    amount_credit=amount)
    if acc_credit.acc_type == ACC_A or acc_credit.acc_type == ACC_AP:
        newLiabilities = acc_credit.liabilities + amount
        newBalance = acc_credit.assets - newLiabilities
        newData = {'liabilities': newLiabilities, 'balance': newBalance}
        accSerializer = AccountSerializer(acc_credit, data=newData)
        
        acc_history['end_liabilities'] = newLiabilities
        acc_history['end_balance'] = newBalance
        
        if accSerializer.is_valid():
            accSerializer.save()
    else:
        newLiabilities = acc_credit.liabilities + amount
        newBalance = newLiabilities - acc_credit.assets
        newData = {'liabilities': newLiabilities, 'balance': newBalance}
        accSerializer = AccountSerializer(acc_credit, data=newData)
        
        acc_history['end_liabilities'] = newLiabilities
        acc_history['end_balance'] = newBalance
        
        if accSerializer.is_valid():
            accSerializer.save()
            
    accountHistorySerializer = AccountHistorySerializer(data=acc_history)
    accountHistorySerializer.run_validation(data=acc_history)
    if accountHistorySerializer.is_valid():
        accountHistorySerializer.save()

    if acc_credit.parent != None:
        creditAcc(acc_credit.parent, amount, id_assign_detail)


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

    with open("short_ledger.txt", "r") as fp:
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

    return Response(status=status.HTTP_201_CREATED)


def assignData(assign_data):
    lstAssign = assign_data['lstAssgn']
    total = assign_data['total']
    sum = 0
    
    print(assign_data)
    print(lstAssign)
    
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
            sum += amount
            debitAcc(debit_acc, amount, id_assign_detail)
            creditAcc(credit_acc, amount, id_assign_detail)
    if abs(total - sum) >= 0.0001:
        raise Exception("Accounting data mismatch")
    # raise Exception('Test exception')
    

def getOrCreateAcc(parent: str,
                   name: str):
    try:
        account = Account.objects.get(pk=parent+name)
        return account
    except Exception:
        aParent = Account.objects.get(pk=parent)
        s = aParent.name + name
        s = aParent.name+name
        a = Account(name=s,
                    acc_type=aParent.acc_type,
                    parent=aParent,
                    description=s)
        a.save()
        return a


def createGroup(parent:str ,
                suffix:str ,
                start:str ,
                end: str):
    aParent = Account.objects.get(pk=parent)
    for i in range(int(start), int(end)+1):
        s = aParent.name+suffix+str(i).zfill(LZ)
        a = Account(name=s,
                    acc_type=aParent.acc_type,
                    parent=aParent,
                    description=s)
        a.save()


