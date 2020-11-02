from rest_framework import serializers
import xml.etree.ElementTree as ET
from formal.grammar import build_from_tree
import re

from formal.models import ProofModel
from formal.rules_inference import SentenceProof


class SentenceSerializer(serializers.Serializer):
    xml = serializers.CharField()

    def validate(self, attrs):
        try:
            xml = ET.fromstring(attrs["xml"])
        except ET.ParseError:
            raise serializers.ValidationError("error parsing xml")
        try:
            sentence = build_from_tree(xml)
        except Exception:
            raise serializers.ValidationError("error building sentence from tree")
        return {"xml": attrs["xml"], "sentence": sentence}

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


def transform_proofs(proofs):
    res_list = []
    for proof in proofs:
        res = to_tuple_int(proof)
        if res is None:
            res = int(proof)
        res_list.append(res)
    return res_list


class SentenceProofSerializer(serializers.Serializer):
    rule = serializers.CharField()
    proofs = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    args = serializers.ListField(child=serializers.CharField(), allow_empty=True)

    def validate_proofs(self, value):
        for proof in value:
            res = pattern_tuple_int.fullmatch(proof)
            if res is None:
                try:
                    res = int(proof)
                except Exception:
                    raise serializers.ValidationError(
                        "proof is neither an int tuple nor a int"
                    )
        return value

    def create(self, validated_data):
        return SentenceProof(
            rule=validated_data["rule"],
            proofs=transform_proofs(validated_data["proofs"]),
            args=validated_data["args"],
        )

    def update(self, instance, validated_data):
        return SentenceProof(
            rule=validated_data["rule"],
            proofs=transform_proofs(validated_data["proofs"]),
            args=validated_data["args"],
        )


def sentence_proof_data(data):
    return data["rule"] + str(data["proofs"]) + str(data["args"])


def validate_positive(value):
    if value < 0:
        raise serializers.ValidationError("not a positive value")


class ProofModelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    sentence = SentenceSerializer()
    sentence_proof = SentenceProofSerializer(allow_null=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=ProofModel.objects.all(), allow_null=True
    )
    parent_position = serializers.IntegerField(validators=[validate_positive])

    def create(self, validated_data):
        proof = ProofModel(
            sentence=validated_data["sentence"]["xml"],
            sentence_proof=sentence_proof_data(validated_data["sentence_proof"]),
            parent=validated_data["parent"],
            parent_position=validated_data["parent_position"],
        )
        proof.save()
        return proof

    def update(self, instance, validated_data):
        instance.sentence = validated_data["sentence"]["xml"]
        instance.sentence_proof = sentence_proof_data(validated_data["sentence_proof"])
        instance.parent = validated_data["parent"]
        instance.parent_position = validated_data["parent_position"]
        instance.save()
        return instance
