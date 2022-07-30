from django.db import transaction
from acc.con import A411, A501, A712, LZ
from acc.utils import getOrCreateAcc, assignData

from .models import Subscriber, Tax, AssignedTax, Group


def createSubscriber(group: Group,
                     start: str,
                     end: str,
                     suffix: str ='a'):
    parentAcc = getOrCreateAcc(A411, group.name)
    for i in range(int(start), int(end)+1):
        s = suffix+str(i).zfill(LZ)
        a = getOrCreateAcc(parentAcc.name, s)
        subscriber = Subscriber(group=group,
                                name=group.name+s,
                                account=a)
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
            assignedTaxes = subscriber.assignedTaxes.filter(description=description)
            if(len(assignedTaxes) > 0):
                continue
            at = AssignedTax(tax=tax, amount=tax.amount, description=description)
            at.save()
            subscriber.assignedTaxes.add(at)
            subscriber.save()
            assign_id = аssign1Data(subscriber.account.name,
                                    '712',
                                    tax.amount,
                                    description)
            at.assign_debit_id = assign_id
            at.save()


def createGroup(name: str, parent_name: str = ''):
    
    group: Group = Group(name=parent_name+name)
    
    if parent_name != '':
        parentGroup: Group = Group.objects.get(name=parent_name)
        group.a411 = getOrCreateAcc(parentGroup.a411.name, name)
        group.a501 = getOrCreateAcc(parentGroup.a501.name, name)
        group.a712 = getOrCreateAcc(parentGroup.a712.name, name)
        group.parent_group = parentGroup
    else:
        group.a411 = getOrCreateAcc(A411, name)
        group.a501 = getOrCreateAcc(A501, name)
        group.a712 = getOrCreateAcc(A712, name)
        
    group.save()
    
    return group


def subsInit(request):
    with transaction.atomic():
        # tax1 = Tax(name="Tax 1", amount=20)
        # tax1.save()
        # createGroup('b001')
        # createGroup('e01', parent_name='b001')
        # g = Group.objects.get(pk='b001e01')
        # createSubscriber(g, '1', '4')
        tax1 = Tax.objects.all()[0]
        testSubscribeTax(tax1)
        testAssignTax(tax1)
        pass
        
