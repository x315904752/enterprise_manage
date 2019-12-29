from enterprise_manage.settings.base import *


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_DB,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWORD,
        'HOST': MYSQL_IP,
        'PORT': MYSQL_PORT,
        'OPTIONS': {
            "init_command": "SET foreign_key_checks = 0;",
        }
    }
}
