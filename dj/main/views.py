# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from jsonview.decorators import json_view
from django.shortcuts import render
import json
from quiz.models.models import Room
import brukva
bclient = brukva.Client()
bclient.connect()
from django.http import HttpResponse, HttpResponseRedirect
from .models import Page
from django.views.decorators.csrf import csrf_exempt
from account.models import Profile
# Create your views here.
from django.shortcuts import render
from django.db import connection
from dj.settings import SOCKET_SERVER
from chat.models import ChatRoom

# Create your views here.

@json_view 
@csrf_exempt
def socket_online(request):
    with connection.cursor() as cursor:
        jdata = json.loads(request.body)
        #print jdata
        cursor.execute('UPDATE account_profile set is_online=False where is_online=True')
        #print len(jdata)
        for u in jdata:
            if u != None:
                try:
                    sql = 'UPDATE account_profile set is_online=True where user_id=%d' % u
                    #print sql
                    cursor.execute(sql)
                except:
                    pass
        #print jdata
    return {'status': 0, 'data': jdata}


@json_view 
def user_online(request):
    users = []
    for u in Profile.objects.filter(is_online=True):
        users.append({
            'user_id': u.user_id,
            'username': u.get_username()
        })
    return users





def cert(request):
    return HttpResponse('hLcZHCBseQmkFYXNilEpAaJFJM3LF63pUEhEkTABgdM._H_I45-2XgtE9CQ_-JG_5A20CtRsr6t23FuZAkbvK-4')

def index(request):
    #chat = ChatRoom.objects.first()
    #chat.get_random_question()
    rooms = Room.objects.all()
    try:
        page = Page.objects.get(alias='quiz')
    except:
        page = {}
    return render(request, 'index.html', {
            'rooms' : rooms,
            'page': page,
            'socket_server': SOCKET_SERVER
        })

@json_view    
def ping(request):
    mes = {"ping": "OK"}
    bclient.publish('channel_1', json.dumps(mes)) 
    return {"status": 0}


def change_language(request):
    from django.conf import settings
    from django.utils import translation
    
    _next = request.GET.get('next', None)
    if not _next:
        _next = request.META.get('HTTP_REFERER', None)

    if not _next:
        _next = '/'
    # если уже есть языковой префикс URL, надо убрать его
    for supported_language in settings.LANGUAGES:
        prefix = '/%s/' % supported_language[0]
        if _next.startswith(prefix):
            _next = _next[len(prefix):]
            break
    language = request.GET.get(u'language', None)
    if _next == '/':
        response = HttpResponseRedirect('/')
    else:
        response = HttpResponseRedirect('/%s/%s' % (language, _next))

    if hasattr(request, 'session'):
        request.session['django_language'] = language
    else:
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)

    translation.activate(language)
    return response

def socket_server_processor(request):
    from dj.settings import SOCKET_SERVER
    return {'socket_server': SOCKET_SERVER}