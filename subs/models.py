from turtle import mode
from xml.dom.minidom import CharacterData
from django.db import models
from django.forms import CharField
from acc.con import A411, A501, A712
from acc.models import Account, Assign


class Tax(models.Model):
    name = models.CharField(max_length=40, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class AssignedTax(models.Model):
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    subscriber = models.ForeignKey('Subscriber', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    description = models.CharField(max_length=60, default='')
    assign_debit = models.ForeignKey(
        Assign, blank=True, null=True, on_delete=models.CASCADE, related_name='ad')
    assign_credit = models.ForeignKey(
        Assign, blank=True, null=True, on_delete=models.CASCADE, related_name='ac')
    assign_debit_reversed = models.ForeignKey(
        Assign, blank=True, null=True, on_delete=models.CASCADE, related_name='adr')
    assign_credit_reversed = models.ForeignKey(
        Assign, blank=True, null=True, on_delete=models.CASCADE, related_name='acf')
    # TODO


class Group(models.Model):

    name = models.CharField(max_length=40, null=False,
                            blank=False, unique=True, primary_key=True, default='0')
    a411 = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name='a411')
    a501 = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name='a501')
    a712 = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name='a712')

    parent_group = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)


class Subscriber(models.Model):

    name = models.CharField(max_length=40, null=False,
                            blank=False, unique=True, primary_key=True, default='0')

    account = models.OneToOneField(Account, on_delete=models.CASCADE)  # TODO

    taxes = models.ManyToManyField(Tax)

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, blank=False, null=False, default='')

    def __str__(self) -> str:
        return self.name
