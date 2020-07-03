from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    to_user = models.OneToOneField(
        User,
        verbose_name='用户名',
        on_delete=models.CASCADE,
    )
    leader = models.CharField(verbose_name='领导', max_length=30, blank=True, default='')
    name = models.CharField(verbose_name='姓名', max_length=30)
    mobile_phone = models.CharField(verbose_name='手机', max_length=30, blank=True, null=True)
    email = models.EmailField(verbose_name='邮箱', blank=True, null=True)
    wechat = models.CharField(verbose_name='微信', max_length=30, blank=True, null=True)
    qq = models.CharField(verbose_name='QQ', max_length=30, blank=True, null=True)
    user_photo = models.ImageField(
        verbose_name='头像',
        blank=True,
        upload_to='user-photo/%Y/%m',
        default='user-photo/user_photo_demo.jpg'
    )
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    is_first = models.BooleanField(verbose_name='是否第一次登陆', default=True)
    remark = models.TextField(verbose_name='备注信息', default='')

    class Meta:
        verbose_name = "用户属性"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
