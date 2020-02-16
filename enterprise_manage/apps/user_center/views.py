from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from enterprise_manage.apps.user_center.serializers import *
from enterprise_manage.apps.user_center.models import *


class MyInfoViewSet(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    """
    Retrieve:
        查看当前登陆用户的个人信息
    """
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return UserProfile.objects.get(to_user__exact=self.request.user)

    def get_serializer_class(self):
        return MyInfoRetrieveSerializer


class ChangePasswordViewSet(viewsets.ViewSet):
    """
    Create:
        修改密码
    """
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        new_password = request.data.get('password', None)
        user = request.user
        user.password = make_password(new_password)
        user.userprofile.is_first = False
        user.save()
        user.userprofile.save()
        return Response({'msg': '修改成功'}, status=200)
