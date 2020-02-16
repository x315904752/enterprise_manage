import xadmin
from enterprise_manage.apps.score_center.models import *


class ScoreProjectAdmin(object):
    list_display = ['id', 'name']
    list_editable = ['id', 'name']


xadmin.site.register(ScoreProject, ScoreProjectAdmin)


class ScoreOptionAdmin(object):
    list_display = ['id', 'name', 'to_score_project', 'score_min', 'score_max']
    list_editable = ['id', 'name', 'to_score_project', 'score_min', 'score_max']


xadmin.site.register(ScoreOption, ScoreOptionAdmin)


class ScoreUserProfileAdmin(object):
    list_display = ['id', 'to_score_project', 'to_user_profile', 'order_num']
    list_editable = ['id', 'to_score_project', 'to_user_profile', 'order_num']


xadmin.site.register(ScoreUserProfile, ScoreUserProfileAdmin)


class ScoreResultAdmin(object):
    list_display = ['id', 'to_user_profile', 'create_user', 'to_score_option', 'score_result']
    list_editable = ['id', 'to_score_user_profile', 'create_user', 'score_result']
    list_filter = [
        "create_user",
        "to_score_user_profile__to_user_profile"
    ]    
    def to_user_profile(self, obj):
        try:
            return obj.to_score_user_profile.to_user_profile
        except:
            return ''

xadmin.site.register(ScoreResult, ScoreResultAdmin)


class UserProfileScoreProjectAdmin(object):
    list_display = ['id', 'to_score_project', 'to_user_profile']
    list_editable = ['id', 'to_score_project', 'to_user_profile']
    list_filter = [
        "to_score_project",
        "to_user_profile"
    ]

xadmin.site.register(UserProfileScoreProject, UserProfileScoreProjectAdmin)


