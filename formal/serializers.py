from rest_framework import serializers
import xml.etree.ElementTree as ET
from formal.grammar import build_from_tree
import re

from formal.models import ProofModel


class SentenceSerializer(serializers.Serializer):
    xml = serializers.CharField()

    def validate(self, attrs):
        try:
            xml = ET.fromstring(attrs["xml"])
        except ET.ParseError:
            raise serializers.ValidationError("error parsing xml")
        try:
            sentence = build_from_tree(xml)
        except ValueError:
            raise serializers.ValidationError("error building sentence from tree")
        return {"sentence": sentence}

    def create(self, validated_data):
        return validated_data["sentence"]

    def update(self, instance, validated_data):
        return validated_data["sentence"]


pattern_tuple_int = re.compile("\((\d*,)*\d*\)")


def to_tuple_int(s):
    if not isinstance(s, str):
        return None
    if pattern_tuple_int.fullmatch(s) is not None:
        return tuple(map(int, s[1:-1].split(",")))
    return None


class SentenceProofSerializer(serializers.Serializer):
    rule = serializers.CharField()
    proofs = serializers.ListField(child=serializers.CharField, allow_empty=True)
    args = serializers.ListField(child=serializers.CharField, allow_empty=True)

    def validate_proofs(self, value):
        proofs = []
        for proof in value:
            res = to_tuple_int(proof)
            if res is None:
                try:
                    res = int(proof)
                except ValueError:
                    raise serializers.ValidationError(
                        "proof is neither an int tuple nor a int"
                    )
            proofs.append(res)
        return proofs


class ProofModelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    sentence = SentenceSerializer()
    sentence_proof = SentenceProofSerializer(allow_null=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=ProofModel.objects.all(), allow_null=True
    )
