# -*- coding: utf-8 -*
from __future__ import absolute_import
import sys, django, os
sys.path.append("./enterprise_manage")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")
django.setup()

from enterprise_manage.apps.score_center.models import UserProfileScoreProject
from enterprise_manage.apps.user_center.models import UserProfile


upsp = UserProfileScoreProject.objects.get(id__exact=67)

with open('dqkj_fg', 'r', encoding='UTF-8') as f:
    user_profile = UserProfile.objects.none()
    for i in f.readlines():
        print(i.strip('\n'))
        user_profile = user_profile | UserProfile.objects.filter(name__exact=i.strip('\n'))

print(len(user_profile))
upsp.exclude_user_profile.set(user_profile)
upsp.save()