from django.db import models

# Create your models here.


class Account(models.Model):
    name = models.CharField(max_length=20, null=False,blank=False,unique=True, primary_key=True)
    description = models.CharField(max_length=20, null=False,blank=False,unique=True, default='Balance')
    assets = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    liabilities = models.DecimalField(
        max_digits=10, decimal_places=4, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    parent = models.ForeignKey('self', 
                               default=None, 
                               on_delete=models.PROTECT, 
                               blank=True,
                               null=True)
    
    def debit(self, n):
        pass
