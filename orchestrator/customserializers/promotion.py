from orchestrator.models import Promotion
from rest_framework import serializers

class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Promotion
        fields = ('promotion_description', 'expiration_date')
