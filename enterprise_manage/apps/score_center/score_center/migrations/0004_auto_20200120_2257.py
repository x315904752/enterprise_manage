# Generated by Django 2.1.1 on 2020-01-20 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('score_center', '0003_userprofilescoreproject_exclude_user_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scoreoption',
            options={'verbose_name': '打分选项', 'verbose_name_plural': '打分选项'},
        ),
    ]