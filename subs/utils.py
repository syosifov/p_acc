from django.db import transaction
import decimal
from decimal import Decimal as D
from core.con import A411, A412, A501, A712, LZ
from acc.utils import getOrCreateAcc, assignData

from .models import Subscriber, Tax, AssignedTax, Group


def createSubscriber(group: Group,
                     start: str,
                     end: str,
                     suffix: str ='a'):
    parentAcc411 = getOrCreateAcc(A411, group.name)
    parentAcc412 = getOrCreateAcc(A412, group.name)0
    parentAcc501 = getOrCreateAcc(A501, group.name)
    for i in range(int(start), int(end)+1):
        s = suffix+str(i).zfill(LZ)
        acc411 = getOrCreateAcc(parentAcc411.name, s)
        acc412 = getOrCreateAcc(parentAcc412.name, s)
        acc501 = getOrCreateAcc(parentAcc501.name, s)
        subscriber = Subscriber(group=group,
                                name=group.name+s,
                                a411=acc411,
                                a412=acc412,
                                a501=acc501)
        subscriber.save()


def аssign1Data(debit: str,
                credit: str,
                amount: float,
                description: str):
    ad = {'debit_acc': debit, 'credit_acc': credit, 'amount': amount}
    data = {'description': description,
            'lstAssgn': [ad],
            'total': amount}
    assigned_id = assignData(data)
    return assigned_id


def testSubscribeTax(tax: Tax):
    qs = Subscriber.objects.all()
    for s in qs:
        n = int(s.name[-1])
        if n % 2 == 0:
            s.taxes.add(tax)
        
        
def testAssignTax(tax: Tax):
    qs = Subscriber.objects.all()
    detail = '2022.07.01'
    for subscriber in qs:
        taxes = subscriber.taxes.all()
        
        if tax in taxes:
            description = f'{subscriber.name} - {tax.name} - {detail}'
            assignedTaxes = subscriber.assignedtax_set.filter(description=description)
            if(len(assignedTaxes) > 0):
                continue
            at = AssignedTax(tax=tax, 
                             amount=tax.amount, 
                             description=description,
                             subscriber=subscriber)
            at.save()
            assign_id = аssign1Data(subscriber.a411.name,
                                    subscriber.group.a712.name,
                                    tax.amount,
                                    description)
            at.assign_debit_id = assign_id
            at.save()


def createGroup(name: str, parent_name: str = ''):
    
    group: Group = Group(name=parent_name+name)
    
    if parent_name != '':
        parentGroup: Group = Group.objects.get(name=parent_name)
        group.a411 = getOrCreateAcc(parentGroup.a411.name, name)
        group.a412 = getOrCreateAcc(parentGroup.a412.name, name)
        group.a501 = getOrCreateAcc(parentGroup.a501.name, name)
        group.a712 = getOrCreateAcc(parentGroup.a712.name, name)
        group.parent_group = parentGroup
    else:
        group.a411 = getOrCreateAcc(A411, name)
        group.a412 = getOrCreateAcc(A412, name)
        group.a501 = getOrCreateAcc(A501, name)
        group.a712 = getOrCreateAcc(A712, name)
        
    group.save()
    
    return group


def subsInit(request):
    with transaction.atomic():
        tax1 = Tax(name="Tax 1", amount=20)
        tax1.save()
        createGroup('b001')
        createGroup('e01', parent_name='b001')
        g = Group.objects.get(pk='b001e01')
        createSubscriber(g, '1', '4')
        tax1 = Tax.objects.all()[0]
        testSubscribeTax(tax1)
        testAssignTax(tax1)
    
    
def payTheTax(subscriber: Subscriber,
              amount: D,
              at: AssignedTax) -> D:
    amount_to_pay = at.amount-at.amount_paid
    if amount >= at.amount-at.amount_paid:
        at.paid = True
        at.amount_paid = at.amount
        at.save()
        аssign1Data(subscriber.a501.name,
                    subscriber.a411.name,
                    amount_to_pay,
                    at.description+' paying')
        amount -= amount_to_pay
    else:
        аssign1Data(subscriber.a501.name,
                    subscriber.a411.name,
                    amount,
                    at.description+" partial")
        at.amount_paid += D(amount)
        at.save()
        amount = D(0)
        
    return amount


def payTax(assigned_tax_id: int,
           subscriber_id: str,
           amount):
    amount = D(amount)
    at = AssignedTax.objects.get(pk=assigned_tax_id)
    subscriber = Subscriber.objects.get(pk=subscriber_id)
    amount = payTheTax(subscriber,amount,at)
    
    if amount > D(0):
        аssign1Data(subscriber.a501.name,
                    subscriber.group.a712.name,
                    amount,
                    subscriber.name +" "+ "installment") 
        

def importMoney(subscriber_id,
                amount,
                description):
    amount = D(amount)
    subscriber = Subscriber.objects.get(pk=subscriber_id)
    atx = subscriber.assignedtax_set.filter(paid=False)
    for at in atx:
        amount = payTheTax(subscriber,amount,at)
        
    if amount > D(0):
        аssign1Data(subscriber.a501.name,
                    subscriber.group.a712.name,
                    amount,
                    subscriber.name +" "+ description) 


