from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentification import authentification
from authentification.models import EmailConfirmation, ResetPasswordConfirmation
from authentification.serializers import (
    SignInSerializer,
    TokenUser,
    TokenUserSerializer,
    TokenCheckSerializer,
    CreateAccountSerializer,
    AskResetSerializer,
    ResetPasswordSerializer,
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


class CreateAccount(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = CreateAccountSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["email"]
            frontend_url = serializer.validated_data.pop("frontend_url")
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username, is_active=False, **serializer.validated_data
                )
                EmailConfirmation.create(user, frontend_url)
                return Response(status=status.HTTP_200_OK)
            if not user.is_active:
                try:
                    confirmation = EmailConfirmation.objects.get(user=user)
                    if confirmation.is_valid():
                        return Response(
                            {
                                "detail": "A confirmation email was already sent to that address"
                            },
                            status=status.HTTP_404_NOT_FOUND,
                        )
                    confirmation.delete()
                except EmailConfirmation.DoesNotExist:
                    pass
                user.first_name = serializer.validated_data["first_name"]
                user.last_name = serializer.validated_data["last_name"]
                user.set_password(serializer.validated_data["password"])
                user.save()
                EmailConfirmation.create(user, frontend_url)
                return Response(status=status.HTTP_200_OK)
            return Response(
                {"detail": "A user with that email already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmAccount(APIView):
    permission_classes = [AllowAny]

    def get(self, request, url, format=None):
        try:
            confirmation = EmailConfirmation.objects.get(url=url)
        except EmailConfirmation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not confirmation.is_valid():
            confirmation.delete()
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()
        return Response(status=status.HTTP_200_OK)


class AskReset(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AskResetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data["email"])
            except User.DoesNotExist:
                return Response(
                    {"detail": "No user registered with that email."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            try:
                confirmation = ResetPasswordConfirmation.objects.get(user=user)
                if confirmation.is_valid():
                    return Response(
                        {
                            "detail": "A confirmation email was already sent to that address"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                confirmation.delete()
            except ResetPasswordConfirmation.DoesNotExist:
                pass
            ResetPasswordConfirmation.create(
                user, serializer.validated_data["frontend_url"]
            )
            return Response(status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckReset(APIView):
    permission_classes = [AllowAny]

    def get(self, request, url, format=None):
        try:
            confirmation = ResetPasswordConfirmation.objects.get(url=url)
        except ResetPasswordConfirmation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not confirmation.is_valid():
            confirmation.delete()
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)


class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request, url, format=None):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                confirmation = ResetPasswordConfirmation.objects.get(url=url)
            except ResetPasswordConfirmation.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            user = confirmation.user
            user.set_password(serializer.validated_data["password"])
            user.save()
            confirmation.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
