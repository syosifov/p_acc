from xml.dom.minidom import CharacterData
from django.db import models
from django.forms import CharField
from acc.models import Account, Assign


class Tax(models.Model):
    name = models.CharField(max_length=40, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class AssignedTax(models.Model):
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
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


class Subscriber(models.Model):

    name = models.CharField(max_length=30, null=False,
                            blank=False, unique=True, primary_key=True, default='0')

    account = models.OneToOneField(Account, on_delete=models.CASCADE)  # TODO
    # accountHistory = models.ForeignKey(
    #     AccountHistory, on_delete=models.DO_NOTHING)

    taxes = models.ManyToManyField(Tax)
    assignedTaxes = models.ManyToManyField(AssignedTax)

    def __str__(self) -> str:
        return self.name
