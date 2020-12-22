from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from sets.serializers import AskSerializer


class Ask(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AskSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
