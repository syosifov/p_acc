from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from .models import Account, Assign

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        
        
class AssignSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Assign
        fields = '__all__'
        
        