from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from mapros import authentification
from mapros.serializers import SignInSerializer, UserSerializer


@api_view(["POST"])
@permission_classes(
    (AllowAny,)
)  # here we specify permission by default we set IsAuthenticated
def signin(request):
    signin_serializer = SignInSerializer(data=request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
    user_serialized = UserSerializer(user)
    return Response({"token": token.key, "user": user_serialized.data})


@api_view(["GET"])
def hello_world(request):
    return Response({"msg": "hello world"}, status=status.HTTP_200_OK)
