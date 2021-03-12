from rest_framework import serializers


class AskStateSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=False)
    hypotheses = serializers.ListField(child=serializers.CharField(), allow_empty=False)
    goal = serializers.CharField(allow_blank=False)
    proofs = serializers.ListField(child=serializers.CharField(), allow_empty=True)
