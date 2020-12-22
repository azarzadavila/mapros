from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class Ask(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        return Response(
            {"answer": "\\frac{\\alpha}{\\beta}"}, status=status.HTTP_200_OK
        )
