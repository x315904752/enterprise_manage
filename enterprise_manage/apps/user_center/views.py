from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

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
