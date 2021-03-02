from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from leanserver.serializers import SyncSerializer, StateAtSerializer


class Sync(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        print(request.data)
        serializer = SyncSerializer(data=request.data)
        if serializer.is_valid():
            # TODO sync
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StateAt(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = StateAtSerializer(data=request.data)
        if serializer.is_valid():
            # TODO stateAt
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Start(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # TODO start
        return Response(status=status.HTTP_200_OK)


class End(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # TODO end
        return Response(status=status.HTTP_200_OK)
