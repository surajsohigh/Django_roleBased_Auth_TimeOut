
from rest_framework import serializers
from my_app.models import *
from rest_framework.serializers import ValidationError
from django.contrib.auth import authenticate


# Serializer for user registration
class MyUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'role']

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)
    

# Serializer for user login
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'password']

    def validate(self, attrs):
        return attrs




