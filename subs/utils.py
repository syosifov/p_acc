from unicodedata import name
from acc.con import A411, LZ
from acc.utils import getOrCreateAcc

from .models import Subscriber


def createSubscriber(suffix:str,
                     start:str,
                     end: str):
    for i in range(int(start), int(end)+1):
        s = suffix+str(i).zfill(LZ)
        a = getOrCreateAcc(A411,s)
        subscriber = Subscriber(name=s,
                                account=a)
        subscriber.save()
