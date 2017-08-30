from orchestrator.models import LoginUser, AppUser
from orchestrator.serializers import LoginUserSerializer, AppUserSerializer
from rest_framework import generics, status, mixins
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.response import Response
from orchestrator.libs.socket_connection import send_data_to_socket


class LoginUserList(mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        response = send_data_to_socket({'tipo':1, 'data': request.data})
        return Response(response, status=status.HTTP_202_ACCEPTED)


class AppUserList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AppUserDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

    def get(self, request, *args, **kwargs):
        try:
            db_user = AppUser.objects.get(user_token=kwargs['pk'])
            expire_date = db_user.expiry
            if timezone.now() > expire_date:
                db_user.delete()
        except ObjectDoesNotExist:
            pass
        return self.retrieve(request, *args, **kwargs)
