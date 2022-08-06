from rest_framework import serializers

from .models import Tax, AssignedTax, Subscriber


class TaxSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tax
        fields = '__all__'
        
        
class AssignedTaxSerializer(serializers.ModelSerializer):
    
    subscribers = 'SubscriberSerializer'(read_only=True,many=True)
    class Meta:
        model = AssignedTax
        fields = '__all__'


        
class SubscriberSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscriber
        fields = '__all__'
        
