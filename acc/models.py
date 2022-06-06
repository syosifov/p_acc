from django.db import models

# Create your models here.


class Account(models.Model):
    assets = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    liabilities = models.DecimalField(
        max_digits=10, decimal_places=4, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    parent = models.ForeignKey('self', 
                               default=None, 
                               on_delete=models.PROTECT, 
                               blank=True,
                               null=True)
