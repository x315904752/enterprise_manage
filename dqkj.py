# -*- coding: utf-8 -*
from __future__ import absolute_import
import sys, django, os
sys.path.append("./enterprise_manage")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")
django.setup()

from enterprise_manage.apps.score_center.models import UserProfileScoreProject, ScoreUserProfile
from enterprise_manage.apps.user_center.models import UserProfile


s = UserProfile.objects.none()
for j in ScoreUserProfile.objects.filter(to_score_project_id__exact=6):
    s = s | UserProfile.objects.filter(id__exact=j.to_user_profile.id)
print(s)
with open('caiwu_fz.txt', 'r', encoding='UTF-8') as f:

    for i in f.readlines():
        user_profile = UserProfile.objects.get(name__exact=i.split()[0])
        a = UserProfileScoreProject.objects.get(to_score_project_id__exact=6,  to_user_profile__exact=user_profile)
        d = UserProfile.objects.none()
        for k in s:
            if UserProfile.objects.get(name__exact=i.split()[1]) != k:
                d = d | UserProfile.objects.filter(id__exact=k.id)
        a.exclude_user_profile.set(d)
        a.save()

