from orchestrator.serializers import DeliverRequestSerializer
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from orchestrator.libs.socket_connection import send_data_to_socket


class OrderUpdate(mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = DeliverRequestSerializer

    def post(self, request, *args, **kwargs):
        response = send_data_to_socket(request.data)

        return Response(response, status=status.HTTP_202_ACCEPTED)
