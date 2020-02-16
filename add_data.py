# -*- coding: utf-8 -*
from __future__ import absolute_import
import sys, django, os
sys.path.append("./enterprise_manage")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")
django.setup()
from django.contrib.auth.hashers import make_password

from enterprise_manage.apps.score_center.models import *
from enterprise_manage.apps.user_center.models import *
from django.contrib.auth.models import User

for i in UserProfile.objects.all():
    for j in ScoreUserProfile.objects.all():
        for k in ScoreOption.objects.all():
            ScoreResult.objects.create(to_score_user_profile=j, to_score_option=k, create_user=i, score_result=1.32)

