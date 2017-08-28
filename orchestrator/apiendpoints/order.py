from orchestrator.models import OrderRequested, OrderStored, AppUser
from orchestrator.serializers import OrderRequestedSerializer, OrderStoredSerializer
from orchestrator.apiendpoints.constants import Constants
from rest_framework import generics, status ,mixins
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.response import Response


# ###########
from orchestrator.externalcommunication.apicalls import requestNewOrderToERP, sendOrderToProduction

class OrderRequestedList(mixins.CreateModelMixin,
                    generics.GenericAPIView):

    serializer_class = OrderRequestedSerializer

    def post(self, request, *args, **kwargs):
        # new order serializer
        new_order = OrderRequestedSerializer(data=request.data) 
        if not new_order.is_valid():
            return Response(new_order.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = AppUser.objects.get(user_token=request.data['user_token'])
        except ObjectDoesNotExist:
            return Response({Constants.USER_NOT_FOUND}, status=status.HTTP_406_NOT_ACCEPTABLE)

        order_billed = requestNewOrderToERP({
            'user_token':request.data['user_token'],
            'order':request.data['order']
            })

        if order_billed['type'] != Constants.ANSWER_SUCCESS:
            # error desde el request al ERP
            return Response({order_billed.errors}, status=status.HTTP_400_BAD_REQUEST)

        order_pending = sendOrderToProduction(order_billed)

        if order_pending['type'] != Constants.ANSWER_SUCCESS:
            return Response({order_pending.errors}, status=status.HTTP_400_BAD_REQUEST)

        if order_pending['status'] == Constants.ORDER_DONE:
            return Response(order_pending, status=status.HTTP_202_ACCEPTED)
        
        order = OrderStoredSerializer(data=order_pending)#, context={'request':request})

        if order.is_valid():
            order.save(user_token=user)
            return Response(order.data, status=status.HTTP_202_ACCEPTED)

        return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderStoredList(mixins.ListModelMixin,
                    generics.GenericAPIView):
    queryset = OrderStored.objects.all()
    serializer_class = OrderStoredSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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