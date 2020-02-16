# -*- coding: utf-8 -*
from __future__ import absolute_import
import sys, django, os
sys.path.append("./enterprise_manage")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")
django.setup()
from django.contrib.auth.hashers import make_password

from enterprise_manage.apps.user_center.models import UserProfile
from django.contrib.auth.models import User



# with open('peoples.txt', 'r', encoding='UTF-8') as f:
#     for i in f.readlines():
#         is_exist = len(UserProfile.objects.filter(name__exact=i.strip('\n')))
#         if not is_exist:
#             user = User.objects.create(username=i.strip('\n'), password=make_password('1234'))
#             UserProfile.objects.create(to_user=user, name=i.strip('\n'))

for i in User.objects.all():
    i.password=make_password('1234')
    i.save()