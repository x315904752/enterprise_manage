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

# l = ['徐丽晨', '邱梓杭', '袁家惠', '许珂', '陈芸贇', '成玉维', '童玲', '王丹', '李静', '朱光梅']
# l = ['王春霞', '吕海英', '张敏']
l = ['王萍']

for i in l:
    a = User.objects.get(username=i)
    a.userprofile.is_first = True
    a.userprofile.save()
    a.password=make_password('1234')
    a.save()
