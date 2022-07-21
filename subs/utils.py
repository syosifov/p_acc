from acc.con import A411, LZ
from acc.utils import getOrCreateAcc

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
