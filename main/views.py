from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from leanclient import client_wrapper
from main.manager import (
    Manager,
    extract_goals,
    extract_variable,
    extract_error,
    lean_variable_to_nat,
    lean_goal_to_nat,
)
from main.serializers import AskStateSerializer


def add_all_manager(name, goal, hypotheses, proofs):
    manager = Manager()
    manager.theorem_name = name
    for hyp in hypotheses:
        manager.add_hypothesis(hyp)
    manager.set_initial_goal(goal)
    for proof in proofs:
        manager.add_proof_line(proof)
    return manager


def write_to_lean(manager):
    file = open(client_wrapper.LEAN_DIR_SRC + "result.lean", "w")
    try:
        text, lines = manager.to_lean()
        file.write(text)
    finally:
        file.close()
    return text, lines


def get_goals(manager, states):
    goals = extract_goals(states)
    initial_goal = goals[0]
    goals = goals[1:]
    initial_goal = lean_goal_to_nat(initial_goal, manager.initial_context)
    goals_nat = []
    for i in range(len(goals)):
        if goals[i]:
            goal = lean_goal_to_nat(goals[i], manager.contexts[i])
        else:
            goal = ""
        goals_nat.append(goal)
    return initial_goal, goals_nat


def get_sentences(manager, states):
    states = states[1:]  # don't take the initial goal state
    sentences = []
    for i in range(len(states)):
        cur_sentences = []
        for ident in manager.to_extract[i]:
            sentence = extract_variable(states[i], ident)
            if sentence:
                sentence = lean_variable_to_nat(sentence, manager.contexts[i])
                cur_sentences.append({"ident": ident, "sentence": sentence})
        sentences.append(cur_sentences)
    return sentences


def get_error(err):
    return extract_error(err)


def get_hypotheses_ident(manager):
    return manager.ident_hypotheses()


class AskState(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = AskStateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                manager = add_all_manager(
                    serializer.validated_data["name"],
                    serializer.validated_data["goal"],
                    serializer.validated_data["hypotheses"],
                    serializer.validated_data["proofs"],
                )
            except ValueError as e:
                return Response(
                    {"detail": "{}".format(e)}, status=status.HTTP_400_BAD_REQUEST
                )
            text, lines = write_to_lean(manager)
            states, err = client_wrapper.states("result.lean", lines)
            hypotheses_ident = get_hypotheses_ident(manager)
            initial_goal, goals = get_goals(manager, states)
            sentences = get_sentences(manager, states)
            if err:
                err = extract_error(err)
            res = {
                "hypotheses_ident": hypotheses_ident,
                "initial_goal": initial_goal,
                "goals": goals,
                "sentences": sentences,
                "error": err,
            }
            return Response(res, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
