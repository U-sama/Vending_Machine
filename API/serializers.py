# vending_machine/serializers.py

from rest_framework import serializers
from .models import Users, Product

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'password', 'deposit', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Users.objects.create_user(**validated_data)
        user.deposit = 0
        user.is_active = True
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.password))
        instance.deposit = validated_data.get('deposit', instance.deposit)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'productName', 'amountAvailable', 'cost', 'seller']
    
