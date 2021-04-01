from django.contrib.auth.models import User
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
        fields = ["name", "hypotheses", "goal", "owner", "id"]
        read_only_fields = ["owner", "id"]


class ProofForTheoremUserSerializer(serializers.ModelSerializer):
    theorem_statement = TheoremStatementSerializer(read_only=True)

    class Meta:
        model = ProofForTheoremUser
        fields = ["user", "proof", "id", "theorem_statement"]
        read_only_fields = ["id", "user", "theorem_statement"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]


class CreateProofForTheoremUserSerializer(serializers.Serializer):
    users = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=User.objects.all()),
        allow_empty=True,
    )
    theorem_statement = serializers.PrimaryKeyRelatedField(
        queryset=TheoremStatement.objects.all()
    )

    def validate(self, attrs):
        for u in attrs["users"]:
            try:
                ProofForTheoremUser.objects.get(
                    user_id=u, theorem_statement_id=attrs["theorem_statement"]
                )
            except ProofForTheoremUser.DoesNotExist:
                continue
            raise serializers.ValidationError("theorem statement already sent")
        return attrs


class LightTheoremStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheoremStatement
        fields = ["id", "name", "owner"]


class LightProofForTheoremUserSerializer(serializers.ModelSerializer):
    theorem_statement = LightTheoremStatementSerializer()

    class Meta:
        model = ProofForTheoremUser
        fields = ["id", "theorem_statement", "user"]


class ListFormatProofForTheoremUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProofForTheoremUser
        fields = ["id", "user", "theorem_statement"]
