from orchestrator.models import OrderStored
from orchestrator.serializers import DeliverRequestSerializer, OrderStoredSerializer
from rest_framework import generics, status, mixins
# from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from orchestrator.apiendpoints.constants import Constants
from orchestrator.externalcommunication.apicalls import sendNotificationToUsers
from django.forms.models import model_to_dict
import json
import socket


class OrderUpdate(mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = DeliverRequestSerializer

    def post(self, request, *args, **kwargs):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 9000))
        data = request.data
        data = json.dumps(data, ensure_ascii=False)
        sock.sendall(data)
        result = sock.recv(1024)
        print result
        sock.close()

        return Response(result, status=status.HTTP_202_ACCEPTED)
