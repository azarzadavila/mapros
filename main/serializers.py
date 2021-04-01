from rest_framework import serializers

from main.models import TheoremStatement, ProofForTheoremUser


class AskStateSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=False)
    hypotheses = serializers.ListField(child=serializers.CharField(), allow_empty=False)
    goal = serializers.CharField(allow_blank=False)
    proofs = serializers.ListField(child=serializers.CharField(), allow_empty=True)


class TheoremStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheoremStatement
        fields = "__all__"


class ProofForTheoremUserSerializer(serializers.ModelSerializer):
    theorem_statement = TheoremStatementSerializer()

    class Meta:
        model = ProofForTheoremUser
        fields = ["user", "theorem_statement", "proof"]
