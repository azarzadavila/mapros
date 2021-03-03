from rest_framework import serializers


class SyncSerializer(serializers.Serializer):
    txt = serializers.CharField()
    seq_num = serializers.IntegerField()


class StateAtSerializer(serializers.Serializer):
    txt = serializers.CharField()
    line = serializers.IntegerField()
    col = serializers.IntegerField()
    seq_num = serializers.IntegerField()
