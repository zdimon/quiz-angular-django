# -*- coding: utf-8 -*-
import os
from .settings import BASE_DIR

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gamehub',
        'USER': 'postgres',
        'PASSWORD': '1q2w3e',
        'HOST': 'localhost',
    }
}
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '962025118316-j84jb846ci2iguoeo6146as4f8pcp348.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'YSrulr78oGE4s7xiHWXDDdOD'

ALLOWED_HOSTS = ['local.quizer.com.ua']