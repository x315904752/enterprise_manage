from rest_framework import serializers

from enterprise_manage.apps.score_center.models import *


class ScoreResultSerializer(serializers.ModelSerializer):
    user_photo = serializers.CharField(source='user_photo.url')

    class Meta:
        model = UserProfile
        fields = ['name', 'user_photo']
