from orchestrator.models import OrderRequested, OrderStored, AppUser
from orchestrator.serializers import OrderRequestedSerializer, OrderStoredSerializer
from orchestrator.apiendpoints.constants import Constants
from rest_framework import generics, status ,mixins
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.response import Response
from socketIO_client import SocketIO, LoggingNamespace
import socket
import json


# ###########
from orchestrator.externalcommunication.apicalls import requestNewOrderToERP, sendOrderToProduction


class OrderRequestedList(mixins.CreateModelMixin,
                    generics.GenericAPIView):

    serializer_class = OrderRequestedSerializer

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


class OrderStoredList(mixins.ListModelMixin,
                    generics.GenericAPIView):
    queryset = OrderStored.objects.all()
    serializer_class = OrderStoredSerializer

    def get(self, request, *args, **kwargs):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 9000))
        data = "Informacion"
        sock.sendall(data)
        result = sock.recv(1024)
        print result
        sock.close()

        return Response("Solicitud procesada", status=status.HTTP_202_ACCEPTED)

class OrderStoredDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = OrderStored.objects.all()
    serializer_class = OrderStoredSerializer

    def get(self, request, *args, **kwargs):
        try:
            order = OrderStored.objects.get(order_token=kwargs['pk'])
        except ObjectDoesNotExist:
            pass
        return self.retrieve(request, *args, **kwargs)
