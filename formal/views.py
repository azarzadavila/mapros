from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from formal.serializers import SentenceSerializer, TextSentenceSerializer
from formal.grammar import sentence_to_xml


class CheckXmlSentence(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        query_serializer=SentenceSerializer(), responses={200: "", 400: ""}
    )
    def post(self, request, format=None):
        serializer = SentenceSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TextToXmlSentence(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        query_serializer=TextSentenceSerializer(),
        responses={200: {"xml": "sentence in xml format"}, 400: ""},
    )
    def post(self, request, format=None):
        serialiazer = TextSentenceSerializer(data=request.data)
        if serialiazer.is_valid():
            sentence = serialiazer.save()
            try:
                xml = sentence_to_xml(sentence)
            except ValueError:
                return Response(
                    {"xml": "failed to build xml"}, status=status.HTTP_400_BAD_REQUEST
                )
            return Response({"xml": xml}, status=status.HTTP_200_OK)
        return Response(serialiazer.errors, status=status.HTTP_400_BAD_REQUEST)
