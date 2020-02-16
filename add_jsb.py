# -*- coding: utf-8 -*
from __future__ import absolute_import
import sys, django, os
sys.path.append("./enterprise_manage")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")
django.setup()

from enterprise_manage.apps.score_center.models import ScoreUserProfile
from enterprise_manage.apps.user_center.models import UserProfile


with open('jsb.txt', 'r', encoding='UTF-8') as f:
    for i in f.readlines():
        print(i.strip('\n'))
        ScoreUserProfile.objects.create(to_score_project_id=6, to_user_profile=UserProfile.objects.get(name__exact=i.strip('\n')))
