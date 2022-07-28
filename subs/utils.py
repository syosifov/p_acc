from django.db import transaction
from acc.con import A411, LZ
from acc.utils import getOrCreateAcc, assignData

from .models import Subscriber, Tax, AssignedTax


def createSubscriber(parent: str,
                     suffix: str,
                     start: str,
                     end: str):
    parentAcc = getOrCreateAcc(A411, parent)
    for i in range(int(start), int(end)+1):
        s = suffix+str(i).zfill(LZ)
        a = getOrCreateAcc(parentAcc.name, s)
        subscriber = Subscriber(name=parent+s,
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
        if s.name.find('a') < 0:
            continue
        lst = s.name.split('a')
        n = int(lst[len(lst)-1])
        if n % 2 == 0:
            s.taxes.add(tax)

        
        
def testAssignTax(tax: Tax):
    qs = Subscriber.objects.filter(name__startswith='g001a')
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
    pass


def subsInit(request):
    with transaction.atomic():
        tax1 = Tax(name="Tax 1", amount=20)
        tax1.save()
        createSubscriber('g001', 'a', '1', '4')
        testSubscribeTax(tax1)
        testAssignTax(tax1)
        
