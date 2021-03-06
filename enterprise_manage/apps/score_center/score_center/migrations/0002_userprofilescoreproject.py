# Generated by Django 2.1.1 on 2020-01-18 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0002_userprofile_leader'),
        ('score_center', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileScoreProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_score_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='score_center.ScoreProject', verbose_name='关联打分项目')),
                ('to_user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_center.UserProfile', verbose_name='关联用户')),
            ],
            options={
                'verbose_name': '用户参与的打分项目',
                'verbose_name_plural': '用户参与的打分项目',
            },
        ),
    ]
