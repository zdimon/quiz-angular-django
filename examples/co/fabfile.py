# -*- coding: utf-8 -*-
from fabric.api import *
import os
from contextlib import contextmanager as _contextmanager
        
def production_env():
    """Окружение для продакшена"""
#    env.hosts = ['chat.mirbu.com']
#    env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa.pub')]  # Локальный путь до файла с ключами
    env.user = 'zdimon'  # На сервере будем работать из под пользователя "webmaster"
    env.project_root = '/home/zdimon/co_ve/co'  # Путь до каталога проекта (на сервере)
    env.password = '1q2w3e'
    env.activate = 'source /home/zdimon/co_ve/bin/activate'


env.hosts = ['korova.mirbu.com']
env.port =  22

@_contextmanager
def virtualenv():
    with cd(env.project_root):
        with prefix(env.activate):
            yield




def deploy():
    production_env()  # Инициализация окружения
    with virtualenv():
        run('git pull') # Пуляемся из репозитория
        run('pip install -r requirements.txt') # ставим пакеты
        #run('bower install')
        run('./manage.py collectstatic --noinput') # Собираем статику
        run('./manage.py migrate')
        #run('sudo service uwsgi restart')
        #run('find . -name "*.mo" -print -delete')  # Чистим старые скомпиленные файлы gettext'а
        #run('./manage.py compilemessages')  # Собираем новые файлы gettext'а
        run('sudo supervisorctl restart all')

