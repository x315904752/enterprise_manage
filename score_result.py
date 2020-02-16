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

f = open('zbcn_jg.txt', 'w')
print('#' * 40)

for i in ScoreUserProfile.objects.filter(to_score_project_id__exact=1):
    pz = 0
    pz_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=160)
    for j in pz_score:
        pz += j.score_result
#    print(i.to_user_profile.name, (pz/len(pz_score)*0.1))
    kls = 0
    kls_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=161)
    for k in kls_score:
        kls += k.score_result
#    print(i.to_user_profile.name, (kls/len(kls_score)))
    hhl = 0
    hhl_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=162)
    for l in hhl_score:
        hhl += l.score_result

    qt = 0
    qt_num = 0
    qt_score = ScoreResult.objects.filter(to_score_user_profile__exact=i)
    for m in qt_score:
        if m.create_user.id != 160 and m.create_user.id != 161 and m.create_user.id != 162:
            qt += m.score_result
            qt_num += 1
#    print(i.to_user_profile.name, (qt/len(qt_score)))
    pz_result, kls_result, hhl_result, qt_result = 0, 0, 0, 0
    if len(pz_score):
        pz_result = str(pz/len(pz_score)*0.25)
    if len(kls_score):
        kls_result = str(kls/len(kls_score)*0.25)
    if len(hhl_score):
        hhl_result = str(hhl/len(hhl_score)*0.25)
    if qt_num:
        qt_result = str(qt/qt_num*0.25)
    all_score = float(pz_result) + float(kls_result) + float(hhl_result) + float(qt_result)
    print(i.to_user_profile.name, pz_result, kls_result, hhl_result, qt_result, all_score)


print('#' * 40)
for i in ScoreUserProfile.objects.filter(to_score_project_id__exact=2):
    pz = 0
    pz_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=160)
    for j in pz_score:
        pz += j.score_result
#    print(i.to_user_profile.name, (pz/len(pz_score)*0.1))
    kls = 0
    kls_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=161)
    for k in kls_score:
        kls += k.score_result
#    print(i.to_user_profile.name, (kls/len(kls_score)))
    hhl = 0
    hhl_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=162)
    for l in hhl_score:
        hhl += l.score_result

    dqzz = 0
    dqzz_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=154)
    for m in dqzz_score:
        dqzz += m.score_result

    qt = 0
    qt_num = 0
    qt_score = ScoreResult.objects.filter(to_score_user_profile__exact=i)
    for m in qt_score:
        if m.create_user.id != 160 and m.create_user.id != 161 and m.create_user.id != 162:
            qt += m.score_result
            qt_num += 1
#    print(i.to_user_profile.name, (qt/len(qt_score)))
    pz_result, kls_result, dqzz_result, hhl_result, qt_result = 0, 0, 0, 0, 0
    if len(pz_score):
        pz_result = str(pz/len(pz_score)*0.25)
    if len(kls_score):
        kls_result = str(kls/len(kls_score)*0.2)
    if len(hhl_score):
        hhl_result = str(hhl/len(hhl_score)*0.15)
    if len(dqzz_score):
        dqzz_result = str(dqzz/len(dqzz_score)*0.15)
    if qt_num:
        qt_result = str(qt/qt_num*0.15)

    all_score = float(pz_result) + float(kls_result) + float(hhl_result) + float(dqzz_result) + float(qt_result)
    print(i.to_user_profile.name, pz_result, kls_result, hhl_result, dqzz_result, qt_result, all_score)


