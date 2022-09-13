from pyexpat import model
from rest_framework import serializers

from .models import Merchant


class EpayRequestSerializer(serializers.Serializer):
    MIN = serializers.CharField()
    INVOICE = serializers.CharField()
    # AMOUNT = serializers.DecimalField()
    AMOUNT = serializers.CharField()
    EXP_TIME = serializers.CharField()
    DESCR = serializers.CharField()
    ENCODED = serializers.CharField()
    CHECKSUM = serializers.CharField()
    PAGE = serializers.CharField()
    ENCODING = serializers.CharField()
    
    
class MerchantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Merchant
        fields = '__all__'
        
