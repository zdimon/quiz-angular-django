# -*- coding: utf-8 -*-
"""
Django settings for co project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
DEBUG = False
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
from os.path import abspath, dirname, basename, join, split
from django.utils.translation import ugettext_lazy as _

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2isf5b9fg&0+mtmxnnnb8)unuvmq%jf@1(=++9-whgrb2%h79p'

# SECURITY WARNING: don't run with debug turned on in production!


TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

LANGUAGES = (
    ('ru', _('Russian')),
    ('en', _('English')),
)

LANGUAGE_CODE = 'ru-ru'

LOCALE_PATHS = (
        join(BASE_DIR, 'locale'),
    )


ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
YANDEX_TRANSLATE_KEY = 'trnsl.1.1.20140521T130035Z.1014ae2799c685e3.97b1345108ab3a8520d96f730016a9dac947049b'
ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE = 'en'
ROSETTA_MESSAGES_SOURCE_LANGUAGE_NAME = 'English'


# Application definition

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
)


INSTALLED_APPS = (
    'grappelli',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    'registration',
    'widget_tweaks',
    'django.contrib.comments',
    'django.contrib.sites',
    'taggit',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'djcelery',
    'mptt',
    'sorl.thumbnail',
    'easy_thumbnails',
    'image_cropping',
    'ckeditor',
    'south',
    'course',
    'django_sockjs_tornado',
    'django_ajax',
    'ajax_upload',
    'compressor',
    'social_auth',
    'main',
    'rosetta',
    'liqpay',
    'videolearn',
    'modeltranslation',
    'redactor'
)

REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = 'uploads/'


SITE_ID = 1

MIDDLEWARE_CLASSES = (

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',


)

TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.request',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.i18n',
        'django.contrib.messages.context_processors.messages',

)



ROOT_URLCONF = 'co.urls'

WSGI_APPLICATION = 'co.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/



TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static')

COMPRESS_ROOT = '/static/compress'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
    )




MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_CONFIGS = {

    'small': {
    'toolbar': 'Basic',
    },

    'default': {
    'toolbar': 'Full',
    'height': 300,
    'width': 700,
    },

    'advanced': {
    'toolbar': 'Uni',
    'height': 300,
    'width': 700,
    },


}


ACCOUNT_ACTIVATION_DAYS = 3
AUTH_PROFILE_MODULE = ''

AUTHENTICATION_BACKENDS = (
    

    # Social auth backends
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.contrib.vk.VKOAuth2Backend',
    'social_auth.backends.contrib.odnoklassniki.OdnoklassnikiBackend',
    'social_auth.backends.contrib.mailru.MailruBackend',
    'social_auth.backends.twitter.TwitterBackend',
    'main.auth.ProfileUserModelBackend', 
)


import random
# Если имя не удалось получить, то можно его сгенерировать
SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice(['Darth_Vader', 'Obi-Wan_Kenobi', 'R2-D2', 'C-3PO', 'Yoda'])
# Разрешаем создавать пользователей через social_auth
SOCIAL_AUTH_CREATE_USERS = True

# Перечислим pipeline, которые последовательно буду обрабатывать респонс 
SOCIAL_AUTH_PIPELINE = (
    # Получает по backend и uid инстансы social_user и user
    'social_auth.backends.pipeline.social.social_auth_user',
    # Получает по user.email инстанс пользователя и заменяет собой тот, который получили выше.
    # Кстати, email выдает только Facebook и GitHub, а Vkontakte и Twitter не выдают
    'social_auth.backends.pipeline.associate.associate_by_email',
    # Пытается собрать правильный username, на основе уже имеющихся данных
    'social_auth.backends.pipeline.user.get_username',
    # Создает нового пользователя, если такого еще нет
    'social_auth.backends.pipeline.user.create_user',
    # Пытается связать аккаунты
    'social_auth.backends.pipeline.social.associate_user',
    # Получает и обновляет social_user.extra_data
    'social_auth.backends.pipeline.social.load_extra_data',
    # Обновляет инстанс user дополнительными данными с бекенда
    'social_auth.backends.pipeline.user.update_user_details'
)


#GOOGLE_CONSUMER_KEY          = '964638688967-ejdq7i76hq7oms8j2ap3fm9rst921p3o.apps.googleusercontent.com'
#GOOGLE_CONSUMER_SECRET       = 'ghh0WuZk0xvoGHOtbWsfsoD4'
SOCIAL_AUTH_USER_MODEL = 'main.UserProfile'

SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/accounts/profile/'
LOGIN_ERROR_URL    = '/'

AUTH_PROFILE_MODULE = 'main.models.UserProfile'
#AUTHENTICATION_BACKENDS = (
#    'django.contrib.auth.backends.ModelBackend',
#    
#)


from local import *

from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS


SOCKJS_CLASSES = (
        'course.tornadoserver.ChatConnection',
    )


import djcelery
djcelery.setup_loader()
BROKER_URL = 'redis://localhost:6379/0'


CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_CONFIGS = {

    'small': {
    'toolbar': 'Basic',
    },

    'default': {
    'toolbar': 'Full',
    'height': 300,
    'width': 700,
    },

    'advanced': {
    'toolbar': 'Uni',
    'height': 300,
    'width': 700,
    },


}



