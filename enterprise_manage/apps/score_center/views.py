from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from enterprise_manage.apps.score_center.serializers import *
from enterprise_manage.apps.score_center.models import *


class ScorePeopleViewSet(viewsets.ViewSet):
    """
    List:
        查询当前用户需要打分的用户列表
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        to_score_project = request.query_params.get('to_score_project')
        is_deal = request.query_params.get('is_deal', 0)
        all_score_user_profile = ScoreUserProfile.objects.filter(
            to_score_project_id__exact=int(to_score_project)
        ).order_by('order_num')
        # 已经打过分的人的选项列表
        has_score_user = ScoreResult.objects.filter(create_user__exact=request.user.userprofile)

        # 查询已经打过分的人员列表
        result = []
        len_score_option = len(ScoreOption.objects.filter(to_score_project__exact=int(to_score_project)))

        for i in all_score_user_profile:
            result_str = ''
            len_has_core_user = len(has_score_user.filter(to_score_user_profile__to_user_profile=i.to_user_profile))
            for r in has_score_user.filter(to_score_user_profile__to_user_profile=i.to_user_profile).order_by('to_score_option'):
                result_str = result_str + (r.to_score_option.name + ':' + str(r.score_result) + ' | ')
            if is_deal == '1':
                if len_has_core_user == len_score_option:
                    result.append({
                        'to_score_project': to_score_project,
                        'to_user_profile': {"id": i.to_user_profile.id, "name": i.to_user_profile.name},
                        'result': result_str
                    })
            else:
                if len_has_core_user != len_score_option:
                    result.append({
                        'to_score_project': to_score_project,
                        'to_user_profile': {"id": i.to_user_profile.id, "name": i.to_user_profile.name},
                        'result': result_str
                    })
        return Response(result)


class ListScoreViewSet(viewsets.ViewSet):
    """
    List:
        查询我为指定用户的打分情况
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        to_score_project = request.query_params.get('to_score_project')
        to_user_profile = request.query_params.get('to_user_profile')
        score_user_profile = ScoreUserProfile.objects.get(
            to_score_project_id__exact=int(to_score_project),
            to_user_profile_id__exact=int(to_user_profile)
        )
        result = []
        for i in ScoreOption.objects.filter(to_score_project_id__exact=int(to_score_project)):
            has_score_result = ScoreResult.objects.filter(
                to_score_user_profile__exact=score_user_profile,
                to_score_option__exact=i,
                create_user__exact=request.user.userprofile,
            )
            if has_score_result:
                result.append(
                    {
                        "to_score_option": {
                            "id": i.id,
                            "name": i.name
                        },
                        "to_score_user_profile": has_score_result[0].to_score_user_profile.id,
                        "score_result": has_score_result[0].score_result
                    }
                )
            else:
                result.append(
                    {
                        "to_score_option": {
                            "id": i.id,
                            "name": i.name
                        },
                        "to_score_user_profile": score_user_profile.id,
                        "score_result": 0
                    }
                )
        return Response(result)


class ScoreProjectViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    List:
        查看当前的打分项目
    """
    permission_classes = (IsAuthenticated,)

    queryset = ScoreProject.objects.all()
    serializer_class = ScoreProjectSerializer


class ScoreViewSet(viewsets.ViewSet):
    """
    List:
        为用户打分
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        to_score_project = request.query_params.get('to_score_project')
        to_user_profile = request.query_params.get('to_user_profile')
        to_score_option = request.query_params.get('to_score_option')
        score_result = request.query_params.get('score_result')
        score_user_profile = ScoreUserProfile.objects.get(
            to_score_project_id__exact=int(to_score_project),
            to_user_profile_id__exact=int(to_user_profile),
        )
        get_score_result = ScoreResult.objects.get_or_create(
            to_score_user_profile=score_user_profile,
            to_score_option_id=int(to_score_option),
            create_user=request.user.userprofile
        )
        get_score_result[0].score_result = float(score_result)
        get_score_result[0].save()
        return Response({"code": 0, "data": "success", "err": ""})
