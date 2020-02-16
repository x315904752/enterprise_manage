# -*- coding: utf-8 -*
from __future__ import absolute_import
import sys, django, os
sys.path.append("./enterprise_manage")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")
django.setup()
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from enterprise_manage.apps.score_center.models import *
from enterprise_manage.apps.user_center.models import *
from django.contrib.auth.models import User

f = open('gs_jg.txt', 'w')
for i in ScoreUserProfile.objects.all():
    # 刘总
    lz = 0
    lz_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=26)
    for j in lz_score:
        lz += j.score_result
#    print(i.to_user_profile.name, (lz/len(lz_score)*0.1))
    ld = 0
    ld_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user__exact=UserProfile.objects.get(name__exact=i.to_user_profile.leader))
    for k in ld_score:
        ld += k.score_result
#    print(i.to_user_profile.name, (ld/len(ld_score)))
    qt = 0
    qt_num = 0
    qt_score = ScoreResult.objects.filter(to_score_user_profile__exact=i)
    for l in qt_score:
        if l.create_user != UserProfile.objects.get(name__exact=i.to_user_profile.leader) and l.create_user.id != 26:
            qt += l.score_result
            qt_num += 1
#    print(i.to_user_profile.name, (qt/len(qt_score)))
    print(i.to_user_profile.name, str(lz/len(lz_score)*0.1), str(ld/len(ld_score)*0.3), str(qt/len(qt_score)*0.6))
    f.write("{},{},{},{}\n".format(i.to_user_profile.name, str(lz/len(lz_score)*0.1), str(ld/len(ld_score)*0.3), str(qt/qt_num*0.6)))
