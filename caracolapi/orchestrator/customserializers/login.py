from rest_framework import serializers
from orchestrator.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Django User Serializer
    """
    class Meta:
        model = User
        fields = ('url', 'id', 'username')

class LoginUserSerializer(serializers.HyperlinkedModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')
    #highlight = serializers.HyperlinkedIdentityField(vielw_name='snippet-highlight', format='html')
    user = serializers.CharField(allow_blank=False, required=True)
    password = serializers.CharField(allow_blank=False, required=True)

    class Meta:
        model = LoginUser
        fields = ('user', 'password')

class AppUserSerializer(serializers.HyperlinkedModelSerializer):
    orders = serializers.HyperlinkedRelatedField(many=True, view_name='order-detail', read_only=True)
    class Meta:
        model = AppUser
        fields = ('created', 'user_token', 'user_rights', 'expiry', 'orders')