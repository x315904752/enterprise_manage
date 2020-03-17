# -*- coding: utf-8 -*
from __future__ import absolute_import
import sys, django, os
sys.path.append("./enterprise_manage")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")
django.setup()
from django.contrib.auth.hashers import make_password

from enterprise_manage.apps.score_center.models import ScoreResult
from django.contrib.auth.models import User

with open('result.txt', 'w') as f:
    for i in ScoreResult.objects.all():
        f.write('{},{},{},{},{}\n'.format(i.to_score_user_profile.to_score_project.name,
              i.to_score_user_profile.to_user_profile.name,
              i.to_score_option, i.create_user, i.score_result))
