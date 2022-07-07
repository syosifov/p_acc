from django.contrib.auth.models import User
from dataclasses import field, fields
from pyexpat import model
from rest_framework import serializers
from .models import Account, Assign, AssignDetail, AccountHistory


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        

class AssignDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignDetail
        fields = '__all__'
        
        
class AssignSerializer(serializers.ModelSerializer):
    details = AssignDetailSerializer(read_only=True,many=True)
    class Meta:
        model = Assign
        fields = '__all__'
        

class AccountHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHistory
        fields = '__all__'
        

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        # fields = '__all__'
        fields = [
            "id",
            "username",
            "groups",
            "user_permissions"
        ]