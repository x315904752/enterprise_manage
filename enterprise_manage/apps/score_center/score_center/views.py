import operator

from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from enterprise_manage.apps.score_center.serializers import *
from enterprise_manage.apps.score_center.models import *

ZBCN_LIST = ['刘婷婷', '宋琳蓉', '张雪娇', '刘琳', '翁芝瑜', '刘月', '杨瑛琪', '赵晓丽', '王丹', '丁雯']
ZBKJ_LIST = ['顾福曦', '张敏', '马骁坤', '李萌', '蒋双月', '杜岳', '胡晨芳', '李静', '王祎', '刘琳', '朱光梅', '朱煜璇']
# 王海琴 名字错误 萍总该为王萍

FGSCN_LIST = [
    '王卓', '张丹', '宋皎', '徐丽晨', '何斌红', '邱梓杭', '张小翠', '李丽容', '孙继红', '王薇', '许珂', '邵颖华', '刘羽',
    '袁家惠', '汪子涵', '赵彦卜', '任学锋', '武淑娟', '陈芸贇', '傅丽莹', '王颖', '童玲', '李苹', '王海芹', '成玉维',
    '陆雅玲', '陈雪梅', '杨韩', '隋秀月', '曾云'
]
DQKJ_LIST = ['高咏梅', '李燕欢', '王春霞', '张运开', '李媛媛', '吕海英']

caiwu_fz = {}
dqkj_fz = {}
with open('caiwu_fz.txt', 'r', encoding='UTF8') as f:
    for c in f.readlines():
        caiwu_fz[c.split()[0]] = {'dqhz': c.split()[1], 'dqzz': c.split()[2].strip('\n')}
        dqkj_fz.setdefault(c.split()[1], []).append(c.split()[0])


class ScorePeopleViewSet(viewsets.ViewSet):
    """
    List:
        查询当前用户需要打分的用户列表
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        to_score_project = request.query_params.get('to_score_project')
        is_deal = request.query_params.get('is_deal', 0)
        result = []

        # 查询当前用户的打分项目
        user_profile_score_project = UserProfileScoreProject.objects.filter(
            to_user_profile__exact=request.user.userprofile,
            to_score_project_id__exact=int(to_score_project)
        )
        if len(user_profile_score_project):
            if is_deal == '0':
                all_score_user_profile = ScoreUserProfile.objects.filter(
                    to_score_project_id__exact=int(to_score_project)
                ).order_by('id')
            else:
                all_score_user_profile = ScoreUserProfile.objects.filter(
                    to_score_project_id__exact=int(to_score_project)
                ).order_by('-id')
            # 已经打过分的人的选项列表
            has_score_user = ScoreResult.objects.filter(create_user__exact=request.user.userprofile)

            # 查询已经打过分的人员列表
            len_score_option = len(ScoreOption.objects.filter(to_score_project__exact=int(to_score_project)))

            for i in all_score_user_profile:
                if i.to_user_profile not in user_profile_score_project[0].exclude_user_profile.all():
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
        else:
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
                        "to_user_profile": has_score_result[0].to_score_user_profile.to_user_profile.id,
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
                        "to_user_profile": score_user_profile.to_user_profile.id,
                        "score_result": ''
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

    def get_queryset(self):
        queryset = ScoreProject.objects.none()
        for i in UserProfileScoreProject.objects.filter(to_user_profile__exact=self.request.user.userprofile):
            queryset = queryset | ScoreProject.objects.filter(id__exact=i.to_score_project.id)
        return queryset


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
        #score_user_profile = ScoreUserProfile.objects.get(
        #    id__exact=int(to_user_profile)
        #)
        get_score_result = ScoreResult.objects.get_or_create(
            to_score_user_profile=score_user_profile,
            to_score_option_id=int(to_score_option),
            create_user=request.user.userprofile
        )
        get_score_result[0].score_result = float(score_result)
        get_score_result[0].save()
        return Response({"code": 0, "data": "success", "err": ""})


class ResultOrderViewSet(viewsets.ViewSet):
    """
    List:
        查看人员排名
    """
    def list(self, request):
        order_result = []
        for sp in ScoreUserProfile.objects.all():
            people_score = 0
            for sr in ScoreResult.objects.filter(to_score_user_profile__exact=sp):
                if sp.to_user_profile.leader == sr.create_user.name:
                    people_score += (sr.score_result * 0.3)
                elif sr.create_user.name == '刘保太':
                    people_score += (sr.score_result * 0.3)
                else:
                    people_score += (sr.score_result * 0.1)
            order_result.append({"name": sp.to_user_profile.name, "score": people_score})
        ordered_result = sorted(order_result, key=operator.itemgetter('score'), reverse=True)
        return Response(ordered_result)


class Project_1(viewsets.ViewSet):
    def list(self, request):
        data = []
        for i in ScoreUserProfile.objects.filter(to_score_project_id__exact=1):
            # 萍总分值
            pz = 0
            pz_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=48)
            for j in pz_score:
                pz += (j.score_result * j.to_score_option.score_min /100)
            # 康丽
            kl = 0
            kl_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=49)
            for k in kl_score:
                kl += (k.score_result * k.to_score_option.score_min / 100)

            # 隋欣
            sx = 0
            sx_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=51)
            for l in sx_score:
                sx += (l.score_result * l.to_score_option.score_min / 100)

            # 郝红丽
            hhl = 0
            hhl_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=50)
            for m in hhl_score:
                hhl += (m.score_result * m.to_score_option.score_min / 100)

            # 隋晓海
            sxh = 0
            sxh_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=52)
            for k in sxh_score:
                sxh += (k.score_result * k.to_score_option.score_min / 100)

            pz_result, kl_result, sx_result, hhl_result, sxh_result = 0, 0, 0, 0, 0

            if len(pz_score):
                pz_result = str(pz * 0.3)
            if len(kl_score):
                kl_result = str(kl * 0.2)
            if len(sx_score):
                sx_result = str(sx * 0.2)
            if len(hhl_score):
                hhl_result = str(hhl * 0.15)
            if len(sxh_score):
                sxh_result = str(sxh * 0.15)
            all_score = float(pz_result) + float(kl_result) + float(sx_result) + float(hhl_result) + float(sxh_result)
            data.append({
                "被评分人": i.to_user_profile.name,
                "萍总": round(float(pz_result), 2),
                "康丽": round(float(kl_result), 2),
                "隋欣": round(float(sx_result), 2),
                "郝宏丽": round(float(hhl_result), 2),
                "隋晓海": round(float(sxh_result), 2),
                "总分": round(float(all_score), 2)
            })
        return Response(data)


class Project_2(viewsets.ViewSet):
    def list(self, request):
        data = []
        for i in ScoreUserProfile.objects.filter(to_score_project_id__exact=2):
            # 萍总分值
            pz = 0
            pz_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=48)
            for j in pz_score:
                pz += (j.score_result * j.to_score_option.score_min /100)
            # 康丽
            kl = 0
            kl_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=49)
            for k in kl_score:
                kl += (k.score_result * k.to_score_option.score_min / 100)

            # 郝红丽
            hhl = 0
            hhl_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=50)
            for m in hhl_score:
                hhl += (m.score_result * m.to_score_option.score_min / 100)

            # 总部出纳
            zbcn = 0
            zbcn_num = 0
            for zbcn_people in ZBCN_LIST:
                z = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user__name__exact=zbcn_people)
                if z:
                    zbcn_num += 1
                for k in z:
                    zbcn += (k.score_result * k.to_score_option.score_min / 100)

            # 总部会计
            zbkj = 0
            zbkj_num = 0
            for zbkj_people in (ZBKJ_LIST + ["李媛媛", "吕海英"]):
                z = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user__name__exact=zbkj_people)
                if z:
                    zbkj_num += 1
                for l in z:
                    zbkj += (l.score_result * l.to_score_option.score_min / 100)

            pz_result, kl_result, hhl_result, zbcn_result, zbkj_result = 0, 0, 0, 0, 0

            if len(pz_score):
                pz_result = str(pz * 0.25)
            if len(kl_score):
                kl_result = str(kl * 0.2)
            if len(hhl_score):
                hhl_result = str(hhl * 0.2)
            if zbcn_num:
                zbcn_result = str(zbcn/zbcn_num * 0.2)
            if zbkj_num:
                zbkj_result = str(zbkj/zbkj_num * 0.15)
            all_score = float(pz_result) + float(kl_result) + float(hhl_result) + float(zbcn_result) + float(zbkj_result)
            data.append({
                "被评分人": i.to_user_profile.name,
                "萍总": round(float(pz_result), 2),
                "康丽": round(float(kl_result), 2),
                "郝宏丽": round(float(hhl_result), 2),
                "总部出纳": round(float(zbcn_result), 2),
                "总部会计": round(float(zbkj_result), 2),
                "总分": round(float(all_score), 2)
            })
        return Response(data)



class Project_3(viewsets.ViewSet):
    def list(self, request):

        data = []
        for i in ScoreUserProfile.objects.filter(to_score_project_id__exact=3):
            # 萍总分值
            pz = 0
            pz_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=48)
            for j in pz_score:
                pz += (j.score_result * j.to_score_option.score_min / 100)
            # 康丽
            kl = 0
            kl_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=49)
            for k in kl_score:
                kl += (k.score_result * k.to_score_option.score_min / 100)

            # 郝红丽
            hhl = 0
            hhl_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=50)
            for m in hhl_score:
                hhl += (m.score_result * m.to_score_option.score_min / 100)

            # 分公司出纳
            fgscn = 0
            fgscn_num = 0
            for fgscn_people in FGSCN_LIST:
                z = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user__name__exact=fgscn_people)
                if z:
                    fgscn_num += 1
                for k in z:
                    fgscn += (k.score_result * k.to_score_option.score_min / 100)

            # 大区会计
            dqhz = 0
            dqhz_num = 0

            for dqhz_people in caiwu_fz[i.to_user_profile.name]['dqhz']:
                z = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user__name__exact=dqhz_people)
                if z:
                    dqhz_num += 1
                for l in z:
                    dqhz += (l.score_result * l.to_score_option.score_min / 100)

            # 大区组长
            dqzz = 0
            dqzz_num = 0

            for dqzz_people in caiwu_fz[i.to_user_profile.name]['dqzz']:
                z = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user__name__exact=dqzz_people)
                if z:
                    dqzz_num += 1
                for m in z:
                    dqzz += (m.score_result * m.to_score_option.score_min / 100)

            pz_result, kl_result, hhl_result, fgscn_result, dqhz_result, dqzz_result = 0, 0, 0, 0, 0, 0

            if len(pz_score):
                pz_result = str(pz * 0.25)
            if len(kl_score):
                kl_result = str(kl * 0.2)
            if len(hhl_score):
                hhl_result = str(hhl * 0.15)
            if fgscn_num:
                fgscn_result = str(fgscn/fgscn_num * 0.15)
            if dqhz_num:
                dqhz_result = str(dqhz/dqhz_num * 0.15)
            if dqzz_num:
                dqzz_result = str(dqzz/dqzz_num * 0.10)

            all_score = float(pz_result) + float(kl_result) + float(hhl_result) + float(fgscn_result) + float(dqhz_result) + float(dqzz_result)
            data.append({
                "被评分人": i.to_user_profile.name,
                "萍总": round(float(pz_result), 2),
                "康丽": round(float(kl_result), 2),
                "郝宏丽": round(float(hhl_result), 2),
                "分公司出纳": round(float(fgscn_result), 2),
                "大区会计": round(float(dqhz_result), 2),
                "大区组长": round(float(dqzz_result), 2),
                "总分": round(float(all_score), 2)
            })
        return Response(data)


class Project_4(viewsets.ViewSet):
    def list(self, request):
        data = []
        for i in ScoreUserProfile.objects.filter(to_score_project_id__exact=4):
            # 萍总分值
            pz = 0
            pz_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=48)
            for j in pz_score:
                pz += (j.score_result * j.to_score_option.score_min / 100)

            # 隋欣
            sx = 0
            sx_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=51)
            for l in sx_score:
                sx += (l.score_result * l.to_score_option.score_min / 100)

            # 隋晓海
            sxh = 0
            sxh_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=52)
            for k in sxh_score:
                sxh += (k.score_result * k.to_score_option.score_min / 100)

            # 总部会计 + 大区会计
            zbkjdqkj = 0
            zbkjdqkj_num = 0
            for zbkjdqkj_people in (ZBKJ_LIST + DQKJ_LIST):
                z = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user__name__exact=zbkjdqkj_people)
                if z:
                    zbkjdqkj_num += 1
                for k in z:
                    zbkjdqkj += (k.score_result * k.to_score_option.score_min / 100)

            # 总部出纳
            zbcn = 0
            zbcn_num = 0
            for zbcn_people in ZBCN_LIST:
                z = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user__name__exact=zbcn_people)
                if z:
                    zbcn_num += 1
                for k in z:
                    zbcn += (k.score_result * k.to_score_option.score_min / 100)

            pz_result, sx_result, sxh_result, zbkjdqkj_result, zbcn_result = 0, 0, 0, 0, 0

            if len(pz_score):
                pz_result = str(pz * 0.25)
            if len(sx_score):
                sx_result = str(sx * 0.2)
            if len(sxh_score):
                sxh_result = str(sxh * 0.2)
            if zbkjdqkj_num:
                zbkjdqkj_result = str(zbkjdqkj/zbkjdqkj_num * 0.2)
            if zbcn_num:
                zbcn_result = str(zbcn/zbcn_num * 0.15)
            all_score = float(pz_result) + float(sx_result) + float(sxh_result) + float(zbkjdqkj_result) + float(zbcn_result)
            data.append({
                "被评分人": i.to_user_profile.name,
                "萍总": round(float(pz_result), 2),
                "隋欣": round(float(sx_result), 2),
                "隋晓海": round(float(sxh_result), 2),
                "总部会计+大区会计": round(float(zbkjdqkj_result), 2),
                "总部出纳": round(float(zbcn_result), 2),
                "总分": round(float(all_score), 2)
            })
        return Response(data)


class Project_5(viewsets.ViewSet):
    def list(self, request):
        data = []
        for i in ScoreUserProfile.objects.filter(to_score_project_id__exact=5):
            # 萍总分值
            pz = 0
            pz_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=48)
            for j in pz_score:
                pz += (j.score_result * j.to_score_option.score_min / 100)

            # 隋晓海
            sxh = 0
            sxh_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=52)
            for k in sxh_score:
                sxh += (k.score_result * k.to_score_option.score_min / 100)


            # 总部会计
            zbkj = 0
            zbkj_num = 0
            for zbkj_people in ZBKJ_LIST:
                z = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user__name__exact=zbkj_people)
                if z:
                    zbkj_num += 1
                for l in z:
                    zbkj += (l.score_result * l.to_score_option.score_min / 100)

            pz_result, sxh_result, zbkj_result = 0, 0, 0

            if len(pz_score):
                pz_result = str(pz * 0.4)
            if len(sxh_score):
                sxh_result = str(sxh * 0.3)
            if zbkj_num:
                zbkj_result = str(zbkj/zbkj_num * 0.3)
            all_score = float(pz_result) + float(sxh_result) + float(zbkj_result)
            data.append({
                "被评分人": i.to_user_profile.name,
                "萍总": round(float(pz_result), 2),
                "隋晓海": round(float(sxh_result), 2),
                "总部会计": round(float(zbkj_result), 2),
                "总分": round(float(all_score), 2)
            })
        return Response(data)



class Project_6(viewsets.ViewSet):
    def list(self, request):
        data = []
        for i in ScoreUserProfile.objects.filter(to_score_project_id__exact=6):
            # 萍总分值
            pz = 0
            pz_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=48)
            for j in pz_score:
                pz += (j.score_result * j.to_score_option.score_min / 100)

            # 隋欣
            sx = 0
            sx_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=51)
            for l in sx_score:
                sx += (l.score_result * l.to_score_option.score_min / 100)

            # 隋晓海
            sxh = 0
            sxh_score = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user_id__exact=52)
            for k in sxh_score:
                sxh += (k.score_result * k.to_score_option.score_min / 100)


            # 总部会计 + 大区会计
            zbkjdqkj = 0
            zbkjdqkj_num = 0
            for zbkjdqkj_people in (ZBKJ_LIST + DQKJ_LIST):
                z = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user__name__exact=zbkjdqkj_people)
                if z:
                    zbkjdqkj_num += 1
                for k in z:
                    zbkjdqkj += (k.score_result * k.to_score_option.score_min / 100)

            # 负责省份的分公司出纳
            sffgscn = 0
            sffgscn_num = 0

            for sffgscn_people in dqkj_fz[i.to_user_profile.name]:
                z = ScoreResult.objects.filter(to_score_user_profile__exact=i, create_user__name__exact=sffgscn_people)
                if z:
                    sffgscn_num += 1
                for m in z:
                    sffgscn += (m.score_result * m.to_score_option.score_min / 100)

            pz_result, sx_result, sxh_result, zbkjdqkj_result, sffgscn_result = 0, 0, 0, 0, 0


            if len(pz_score):
                pz_result = str(pz * 0.25)
            if len(sxh_score):
                sx_result = str(sxh * 0.2)
            if len(sxh_score):
                sxh_result = str(sxh * 0.2)
            if zbkjdqkj_num:
                zbkjdqkj_result = str(zbkjdqkj/zbkjdqkj_num * 0.2)
            if sffgscn_num:
                sffgscn_result = str(sffgscn/sffgscn_num * 0.15)
            all_score = float(pz_result) + float(sx_result) + float(sxh_result) + float(zbkjdqkj_result) + float(sffgscn_result)
            data.append({
                "被评分人": i.to_user_profile.name,
                "萍总": round(float(pz_result), 2),
                "隋欣": round(float(sx_result), 2),
                "隋晓海": round(float(sxh_result), 2),
                "总部会计+大区会计": round(float(zbkjdqkj_result), 2),
                "负责省份的分公司出纳": round(float(sffgscn_result), 2),
                "总分": round(float(all_score), 2)
            })
        return Response(data)