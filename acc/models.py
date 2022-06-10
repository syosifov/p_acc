import imp
from django.db import models


# Create your models here.
ACC_A = 0
ACC_P = 1
ACC_AP = 2

class Account(models.Model):
    name = models.CharField(max_length=20, null=False,blank=False,unique=True, primary_key=True, default=' ')
    description = models.CharField(max_length=100, null=False,blank=False,unique=True, default='Balance')
    assets = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    liabilities = models.DecimalField(
        max_digits=10, decimal_places=4, default=0)
    acc_type = models.IntegerField(default=ACC_A)
    balance = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    parent = models.ForeignKey('self', 
                               default=None, 
                               on_delete=models.PROTECT, 
                               blank=True,
                               null=True)
    
    def debit(self, n):
        pass

    def __str__(self) -> str:
        return self.name
    