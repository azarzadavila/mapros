from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from lark.exceptions import UnexpectedInput, VisitError

from sets.serializers import AskSerializer
from sets.proof import Proof
from sets.parser import premise_parse, question_parse
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
                    command = premise_parse(s, proof)
                except (UnexpectedInput, VisitError):
                    return Response(
                        {"message": "unknown command for premise : {}".format(s)},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                invoker.store_command(command)
            try:
                command = question_parse(serializer.validated_data["question"], proof)
            except (UnexpectedInput, VisitError):
                return Response(
                    {
                        "message": "unknown command for question : {}".format(
                            serializer.validated_data["question"]
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            invoker.store_command(command)
            invoker.execute_commands()
            return Response({"answer": str(invoker.result)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
