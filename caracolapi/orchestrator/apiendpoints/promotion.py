#aqui va el endpoint
#el primero de login es el post y el segundo es un get
from orchestrator.externalcommunication.apicalls import requestPromotions
from orchestrator.models import Promotion
from orchestrator.serializers import PromotionSerializer
from rest_framework import generics, mixins, status
from rest_framework.response import Response


class PromotionList(mixins.CreateModelMixin,
                    generics.GenericAPIView):
    serializer_class = PromotionSerializer
    queryset = Promotion.objects.all()
    def get(self, request, *args, **kwargs):
        active_promotions = requestPromotions()
        promotions_to_display = PromotionSerializer(active_promotions, many=True)
        return Response(promotions_to_display.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)