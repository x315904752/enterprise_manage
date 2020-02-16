#!/bin/sh
mkdir /var/log/enterprise_manage
mkdir /opt/proj
mkdir /opt/proj/script
touch /opt/proj/script/uwsgi.pid
touch /opt/proj/script/uwsgi.sock
touch /var/log/enterprise_manage/uwsgi.log
pip3 install -r /opt/enterprise_manage/requirements.txt
python /opt/enterprise_manage/manage.py makemigrations
python /opt/enterprise_manage/manage.py migrate
uwsgi --ini /opt/enterprise_manage/uwsgi.ini
tail -f /var/log/enterprise_manage/uwsgi.log
