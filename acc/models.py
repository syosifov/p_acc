import imp
from django.db import models
from datetime import datetime

# Create your models here.
ACC_A = 0
ACC_P = 1
ACC_AP = 2


class Account(models.Model):
    name = models.CharField(max_length=20, null=False,
                            blank=False, unique=True, primary_key=True, default='0')
    description = models.CharField(
        max_length=100, null=False, blank=False, unique=True, default='Balance')
    assets = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    liabilities = models.DecimalField(
        max_digits=10, decimal_places=4, default=0)
    acc_type = models.IntegerField(default=ACC_AP)
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


class Assign(models.Model):
    debit = models.ForeignKey(
        Account, blank=True, null=True, on_delete=models.PROTECT, related_name='debit')
    credit = models.ForeignKey(
        Account, blank=True, null=True, on_delete=models.PROTECT, related_name='credit')
    description = models.CharField(max_length=200, null=False, blank=False)
    amount = models.DecimalField(
        max_digits=10, decimal_places=4, null=False, blank=False)
    # date = models.DateTimeField(default=datetime.now, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self) -> str:
        return f"{self.debit} {self.credit} {self.amount:6.2f}"
