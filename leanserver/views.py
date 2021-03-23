from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import pexpect
import json

# Create your views here.
from leanserver.serializers import SyncSerializer, StateAtSerializer

# server = pexpect.spawn("lean --server")
server = None


def write_in(s, path="test.lean"):
    file = open(path, "w")
    file.write(s)
    file.close()


def post_command(cmd, seq_num, txt, obj=None):
    write_in(txt)
    to_send = {
        "command": cmd,
        "file_name": "test.lean",
        "seq_num": seq_num,
    }
    if obj is not None:
        to_send.update(obj)
    to_send = json.dumps(to_send)
    server.sendline(to_send)
    to_receive = '\{.+"seq_num":' + str(seq_num) + ".*\}"
    server.expect(to_receive)
    res = server.after.decode()
    res = res.split("\r\n")
    for i in range(len(res)):
        res[i] = json.loads(res[i])
    print(res)
    return Response({"messages": res}, status=status.HTTP_200_OK)


class Sync(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = SyncSerializer(data=request.data)
        if serializer.is_valid():
            return post_command(
                "sync",
                serializer.validated_data["seq_num"],
                serializer.validated_data["txt"],
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StateAt(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = StateAtSerializer(data=request.data)
        if serializer.is_valid():
            return post_command(
                "info",
                serializer.validated_data["seq_num"],
                serializer.validated_data["txt"],
                {
                    "line": serializer.validated_data["line"],
                    "column": serializer.validated_data["col"],
                },
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Start(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # TODO start
        return Response(status=status.HTTP_200_OK)


class End(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # TODO end
        return Response(status=status.HTTP_200_OK)
