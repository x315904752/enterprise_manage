# -*- coding: utf-8 -*
from __future__ import absolute_import
import sys, django, os
sys.path.append("./enterprise_manage")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")
django.setup()

from enterprise_manage.apps.score_center.models import ScoreUserProfile, UserProfileScoreProject
from enterprise_manage.apps.user_center.models import UserProfile



with open('user_project_bind.txt', 'r', encoding='UTF-8') as f:
    for i in f.readlines():
        print(i.strip('\n'))
        UserProfileScoreProject.objects.create(
            to_score_project_id=6,
            to_user_profile=UserProfile.objects.get(name__exact=i.strip('\n'))
        )
