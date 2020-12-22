from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from lark import UnexpectedInput

from sets.serializers import AskSerializer
from sets.proof import Proof
from sets.parser import parse
from sets.invoker import Invoker


class Ask(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AskSerializer(data=request.data)
        if serializer.is_valid():
            invoker = Invoker()
            proof = Proof()
            for s in serializer.validated_data["premises"]:
                try:
                    command = parse(s, proof)
                except UnexpectedInput:
                    return Response(
                        {"message": "unknown command for premise : {}".format(s)}
                    )
                invoker.store_command(command)
            invoker.execute_commands()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
