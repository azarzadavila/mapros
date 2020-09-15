from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from authentification.authentification import ExpiringTokenAuthentication


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


class TokenCheckSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate_token(self, value):
        authentificator = ExpiringTokenAuthentication()
        try:
            authentificator.authenticate_credentials(key=value)
        except AuthenticationFailed as err:
            raise serializers.ValidationError(err.get_full_details())
        return value
