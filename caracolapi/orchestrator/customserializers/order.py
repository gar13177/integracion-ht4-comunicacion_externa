from rest_framework import serializers
from orchestrator.models import *

class OrderRequestedDescriptionSerializer(serializers.Field):
    def from_native(self, data):
        if isinstance(data, list):
            return OrderRequestedDescription(data)
        else:
            msg = self.error_messages['invalid']
            raise ValidationError(msg)

    def to_native(self, obj):
        return obj.order_list

class OrderRequestedDescription(object):
    def __int__(self, order_list):
        self.order_list = order_list

class OrderRequestedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderRequested
        order = OrderRequestedDescriptionSerializer
        fields = ('user_token', 'order', 'request_type')

class OrderStoredSerializer(serializers.HyperlinkedModelSerializer):
    user_token = serializers.ReadOnlyField(source='user_token.user_token')
    class Meta:
        model = OrderStored
        fields = ('created', 'user_token', 'order_token', 'status')
