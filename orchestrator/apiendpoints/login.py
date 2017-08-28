from orchestrator.models import LoginUser, AppUser
from orchestrator.serializers import LoginUserSerializer, AppUserSerializer
from orchestrator.apiendpoints.constants import Constants
from rest_framework import generics, status ,mixins
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.response import Response

# ###########
from orchestrator.externalcommunication.apicalls import requestLoginERP


class LoginUserList(mixins.CreateModelMixin,
                    generics.GenericAPIView):

    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        user_info = requestLoginERP({
                'user':request.data['user'],
                'password':request.data['password']
            })

        if user_info['type'] != Constants.ANSWER_SUCCESS:
            # error desde el request al ERP
            return Response({user_info.errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            db_user = AppUser.objects.get(user_token=user_info['user_token'])
            auth_user = AppUserSerializer(db_user)
            return Response(auth_user.data, status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            pass

        auth_user = AppUserSerializer(data=user_info)
        if auth_user.is_valid():
            auth_user.save()
            return Response(auth_user.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(auth_user.errors, status=status.HTTP_400_BAD_REQUEST)

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