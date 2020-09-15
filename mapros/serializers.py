from django.contrib.auth.models import User
from rest_framework import serializers


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class TokenUser:
    def __init__(self, token, user):
        self.token = token
        self.user = user


class TokenUserSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    user = UserSerializer(required=True)
