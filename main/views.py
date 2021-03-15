from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from leanclient import client_wrapper
from main.manager import Manager, extract_goals, extract_variable
from main.serializers import AskStateSerializer


class AskState(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AskStateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                manager = Manager()
                manager.theorem_name = serializer.validated_data["name"]
                for hyp in serializer.validated_data["hypotheses"]:
                    manager.add_hypothesis(hyp)
                manager.set_initial_goal(serializer.validated_data["goal"])
                for proof in serializer.validated_data["proofs"]:
                    manager.add_proof_line(proof)
                res = {
                    "hypothesesIdent": map(
                        lambda x: "" if x is None else x, manager.ident_hypotheses()
                    ),
                    "initialState": "",
                    "states": [""] * len(serializer.validated_data["proofs"]),
                    "additional": [""] * len(serializer.validated_data["proofs"]),
                }
            except ValueError as e:
                return Response(
                    {"detail": "{}".format(e)}, status=status.HTTP_400_BAD_REQUEST
                )
            file = open(client_wrapper.LEAN_DIR_SRC + "result.lean", "w")
            try:
                text, lines = manager.to_lean()
                file.write(text)
            finally:
                file.close()
            states, err = client_wrapper.states("result.lean", lines)
            goals = extract_goals(states)
            initial_goal = goals[0]
            res["initialState"] = initial_goal
            goals = goals[1:]
            res["states"] = goals
            additional = []
            for i in range(len(states[1:])):
                addi = []
                for var in manager.to_extract[i]:
                    addi.append(extract_variable(states[i + 1], var))
                additional.append(addi)
            res["additional"] = additional
            return Response(res, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
