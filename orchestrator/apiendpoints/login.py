from orchestrator.models import LoginUser, AppUser
from orchestrator.serializers import LoginUserSerializer, AppUserSerializer
from orchestrator.apiendpoints.constants import Constants
from rest_framework import generics, status ,mixins
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.response import Response
import socket
import json


# ###########
from orchestrator.externalcommunication.apicalls import requestLoginERP


class LoginUserList(mixins.CreateModelMixin,
                    generics.GenericAPIView):

    serializer_class = LoginUserSerializer

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

class AppUserList(mixins.ListModelMixin,
                    generics.GenericAPIView):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class AppUserDetail(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
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
