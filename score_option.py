
# -*- coding: utf-8 -*
from __future__ import absolute_import
import sys, django, os
sys.path.append("./enterprise_manage")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")
django.setup()
score_option = ["总结展示", "日常工作", "沟通协作", "积极进取"]

from enterprise_manage.apps.score_center.models import ScoreOption, ScoreProject
from enterprise_manage.apps.user_center.models import UserProfile

for i in score_option:
    for j in ScoreProject.objects.all():
        ScoreOption.objects.create(
            name=i,
            to_score_project=j,
            score_min=0,
            score_max=5
        )




















