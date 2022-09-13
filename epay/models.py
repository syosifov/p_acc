from django.db import models

# Create your models here.


class EpayRequest:
    def __init__(self, MIN, INVOICE, AMOUNT,
                 EXP_TIME, DESCR, ENCODED, CHECKSUM,
                 PAGE="paylogin",
                 ENCODING="utf-8"):
        self.MIN = MIN
        self.INVOICE = INVOICE
        self.AMOUNT = AMOUNT
        self.EXP_TIME = EXP_TIME
        self.DESCR = DESCR
        self.ENCODED = ENCODED
        self.CHECKSUM = CHECKSUM
        self.PAGE = PAGE
        self.ENCODING = ENCODING


        
class Merchant(models.Model):

    min = models.CharField(max_length=40,unique=True)
    secret = models.CharField(max_length=255)

