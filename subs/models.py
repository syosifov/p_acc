from django.db import models
from acc.models import Account, AccountHistory

class Tax(models.Model):
    name = models.CharField(max_length=30,unique=True)
    # amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)


class AssignedTax(models.Model):
    tax = models.ForeignKey(Tax,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
        
        
class Subscriber(models.Model):
    name = models.CharField(max_length=20, null=False,
                            blank=False, unique=True, primary_key=True, default='0')
    
    account = models.OneToOneField(Account,on_delete=models.RESTRICT)
    accountHistory = models.ForeignKey(AccountHistory, on_delete=models.DO_NOTHING)

    parent = models.ForeignKey('self',
                               default=None,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)

    def __str__(self) -> str:
        return self.name        
