from rest_framework import serializers

from .models import Tax, AssignedTax, Subscriber, EpayRequest


class TaxSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tax
        fields = '__all__'
        
        
class AssignedTaxSerializer(serializers.ModelSerializer):
    
    # subscribers = 'SubscriberSerializer'(read_only=True,many=True)
    class Meta:
        model = AssignedTax
        fields = '__all__'


        
class SubscriberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscriber
        fields = '__all__'
        


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