from rest_framework import serializers


class AskSerializer(serializers.Serializer):
    premises = serializers.ListField(child=serializers.CharField())
    question = serializers.CharField()
