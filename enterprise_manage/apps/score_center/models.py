from django.db import models
from enterprise_manage.apps.user_center.models import UserProfile


class ScoreProject(models.Model):
    name = models.CharField(verbose_name='名称', max_length=30)

    class Meta:
        verbose_name = "打分项目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ScoreOption(models.Model):
    name = models.CharField(verbose_name='名称', max_length=30)
    to_score_project = models.ForeignKey(ScoreProject, verbose_name='关联打分项目', on_delete=models.CASCADE)
    score_min = models.IntegerField(verbose_name='最小分值')
    score_max = models.IntegerField(verbose_name='最大分值')

    class Meta:
        verbose_name = "打分项目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ScoreUserProfile(models.Model):
    to_score_project = models.ForeignKey(ScoreProject, verbose_name='关联打分项目', on_delete=models.CASCADE)
    to_user_profile = models.ForeignKey(UserProfile, verbose_name='关联人员', on_delete=models.CASCADE)
    order_num = models.IntegerField(verbose_name='排序', default=0, blank=True)

    class Meta:
        verbose_name = "参与打分的人员表"
        verbose_name_plural = verbose_name
        unique_together = ['to_score_project', 'to_user_profile']

    def __str__(self):
        return self.to_score_project.name


class ScoreResult(models.Model):
    to_score_user_profile = models.ForeignKey(ScoreUserProfile, verbose_name='关联打分人员表', on_delete=models.CASCADE)
    to_score_option = models.ForeignKey(ScoreOption, verbose_name='关联打分项', on_delete=models.CASCADE)
    create_user = models.ForeignKey(UserProfile, verbose_name='打分人员', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    score_result = models.FloatField(verbose_name='分值', blank=True, default=0)

    class Meta:
        verbose_name = "打分结果"
        verbose_name_plural = verbose_name,
        unique_together = ['to_score_user_profile', 'to_score_option', 'create_user']

    def __str__(self):
        return self.to_score_user_profile.to_score_project.name
