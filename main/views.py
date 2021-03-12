from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from main.serializers import AskStateSerializer


class AskState(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AskStateSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response(obj.to_data(), status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
