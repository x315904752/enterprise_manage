from rest_framework import serializers

from enterprise_manage.apps.user_center.models import *


class MyInfoRetrieveSerializer(serializers.ModelSerializer):
    user_photo = serializers.CharField(source='user_photo.url')

    class Meta:
        model = UserProfile
        fields = ['name', 'user_photo', 'is_first']
