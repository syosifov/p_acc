from acc.con import A411, LZ
from acc.utils import getOrCreateAcc, assignData

from .models import Subscriber


def createSubscriber(parent: str,
                     suffix: str,
                     start: str,
                     end: str):
    parentAcc = getOrCreateAcc(A411,parent)
    for i in range(int(start), int(end)+1):
        s = suffix+str(i).zfill(LZ)
        a = getOrCreateAcc(parentAcc.name,s)
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


