from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from authentification import authentification
from authentification.serializers import (
    SignInSerializer,
    TokenUser,
    TokenUserSerializer,
    TokenCheckSerializer,
)


class SignIn(APIView):
    """
    Sign in a user by sending its token
    """

    permission_classes = [
        AllowAny
    ]  # here we specify permission by default we set IsAuthenticated

    @swagger_auto_schema(
        query_serializer=SignInSerializer(), responses={200: TokenUserSerializer},
    )
    def post(self, request, format=None):
        signin_serializer = SignInSerializer(data=request.data)
        if not signin_serializer.is_valid():
            return Response(
                signin_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(
            username=signin_serializer.data["username"],
            password=signin_serializer.data["password"],
        )
        if not user:
            return Response(
                {"detail": "Incorrect username or password."},
                status=status.HTTP_404_NOT_FOUND,
            )
        token = authentification.get_token(user=user)
        token_user = TokenUser(token=token.key, user=user)
        token_user_serialized = TokenUserSerializer(token_user)
        return Response(token_user_serialized.data, status=status.HTTP_200_OK,)


class TokenCheck(APIView):
    """
    Checks the given token
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        query_serializer=TokenCheckSerializer,
        responses={
            200: "The token is correct",
            400: "If the token is incorrect or bad format",
        },
    )
    def post(self, request, format=None):
        token_check_serializer = TokenCheckSerializer(data=request.data)
        if token_check_serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(
            data=token_check_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
