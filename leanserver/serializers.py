from rest_framework import serializers


class SyncSerializer(serializers.Serializer):
    txt = serializers.CharField()

    def create(self, validated_data):
        return validated_data["txt"]


class StateAtSerializer(serializers.Serializer):
    txt = serializers.CharField()
    line = serializers.IntegerField()

    def create(self, validated_data):
        return validated_data
