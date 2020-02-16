import xadmin
from enterprise_manage.apps.user_center.models import *


class UserProfileAdmin(object):
    list_display = ['id', 'name', 'to_user', 'mobile_phone', 'email', 'wechat', 'qq']
    list_editable = ['id', 'name', 'to_user', 'mobile_phone', 'email', 'wechat', 'qq', 'leader']


xadmin.site.register(UserProfile, UserProfileAdmin)
