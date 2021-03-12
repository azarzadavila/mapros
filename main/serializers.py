from rest_framework import serializers


class AskStateSerializer(serializers.Serializer):
    name = serializers.CharField()
    hypotheses = serializers.ListField(child=serializers.CharField())
    goal = serializers.CharField()
    proofs = serializers.ListField(child=serializers.CharField())
    clickOn = serializers.IntegerField()

    # TODO validation on size and clickOn
    def create(self, validated_data):
        return AskStateObj(**validated_data)


class AskStateObj:
    def __init__(self, name, hypotheses, goal, proofs, clickOn):
        self.name = name
        self.hypotheses = hypotheses
        self.goal = goal
        self.proofs = proofs
        self.clickOn = clickOn

    def hypotheses_ident(self):
        res = []
        for i in range(len(self.hypotheses)):
            res.append("H{}".format(i + 1))
        return res

    def states(self):
        res = [""] * len(self.proofs)
        if self.clickOn != -1:
            for i in range(self.clickOn + 1):
                res[i] = "goal updated"
        return res

    def inital_state(self):
        return "goal updated"

    def to_data(self):
        return {
            "hypothesesIdent": self.hypotheses_ident(),
            "initialState": self.inital_state(),
            "states": self.states(),
        }
