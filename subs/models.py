from django.db import models
from acc.models import Account, AccountHistory


class Tax(models.Model):
    name = models.CharField(max_length=30, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class AssignedTax(models.Model):
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)


class Subscriber(models.Model):

    name = models.CharField(max_length=20, null=False,
                            blank=False, unique=True, primary_key=True, default='0')

    account = models.OneToOneField(Account, on_delete=models.CASCADE) # TODO
    # accountHistory = models.ForeignKey(
    #     AccountHistory, on_delete=models.DO_NOTHING)

    taxes = models.ManyToManyField(Tax)
    assignedTaxes = models.ManyToManyField(AssignedTax)

    def __str__(self) -> str:
        return self.name


