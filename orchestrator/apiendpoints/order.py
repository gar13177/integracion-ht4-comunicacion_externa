from orchestrator.models import OrderRequested, OrderStored, AppUser
from orchestrator.serializers import OrderRequestedSerializer, OrderStoredSerializer
from rest_framework import generics, status, mixins
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from orchestrator.libs.socket_connection import send_data_to_socket


class OrderRequestedList(mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = OrderRequestedSerializer

    def post(self, request, *args, **kwargs):
        response = send_data_to_socket(request.data)

        return Response(response, status=status.HTTP_202_ACCEPTED)


class OrderStoredList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = OrderStored.objects.all()
    serializer_class = OrderStoredSerializer

    def get(self, request, *args, **kwargs):
        response = send_data_to_socket(request.data)

        return Response(response, status=status.HTTP_202_ACCEPTED)


class OrderStoredDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = OrderStored.objects.all()
    serializer_class = OrderStoredSerializer

    def get(self, request, *args, **kwargs):
        try:
            order = OrderStored.objects.get(order_token=kwargs['pk'])
        except ObjectDoesNotExist:
            pass
        return self.retrieve(request, *args, **kwargs)
