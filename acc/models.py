import imp
from django.db import models
from datetime import datetime
# from acc.con import *
import acc.con

# Create your models here.


class Account(models.Model):
    name = models.CharField(max_length=20, null=False,
                            blank=False, unique=True, primary_key=True, default='0')
    description = models.CharField(
        max_length=100, null=False, blank=False, unique=True, default='Balance')
    assets = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    liabilities = models.DecimalField(
        max_digits=10, decimal_places=4, default=0)
    acc_type = models.IntegerField(default=acc.con.ACC_AP)
    balance = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    parent = models.ForeignKey('self',
                               default=None,
                               on_delete=models.PROTECT,
                               blank=True,
                               null=True)

    def __str__(self) -> str:
        return self.name


class Assign(models.Model):
    description = models.CharField(max_length=200, null=False, blank=False)
    total = models.DecimalField(
        max_digits=10, decimal_places=4, null=False, blank=False)
    # date = models.DateTimeField(default=datetime.now, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self) -> str:
        return f"{self.description} {self.date} {self.total:6.2f}"


class AssignDetail(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.PROTECT)
    debit_acc = models.ForeignKey(
        Account, blank=True, null=True, on_delete=models.PROTECT, related_name='debit')
    credit_acc = models.ForeignKey(
        Account, blank=True, null=True, on_delete=models.PROTECT, related_name='credit')
    amount = models.DecimalField(
        max_digits=10, decimal_places=4, null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.debit} {self.credit} {self.amount:6.2f}"


class AccountHistory(models.Model):
    name = models.ForeignKey(Account, on_delete=models.PROTECT)
    assignDetail = models.ForeignKey(AssignDetail, 
                                        on_delete=models.PROTECT,
                                        blank=True,
                                        null=True)
    assets = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    liabilities = models.DecimalField(
        max_digits=10, decimal_places=4, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    amaount_debit = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    amount_credit = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    end_assets = models.DecimalField(
        max_digits=10, decimal_places=4, default=0)
    end_liablities = models.DecimalField(
        max_digits=10, decimal_places=4, default=0)
    end_balance = models.DecimalField(
        max_digits=10, decimal_places=4, default=0)
