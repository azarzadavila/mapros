from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


@api_view(["GET"])
def hello_world(request):
    return Response({"msg": "hello world"}, status=status.HTTP_200_OK)
