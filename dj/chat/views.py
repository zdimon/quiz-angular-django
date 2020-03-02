# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import ChatMessage
from quiz.models.models import Question
import json
import brukva
from chat.models import ChatRoom
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext as __
import threading
import time
from .utils import get_current_question, check_answer, get_answers
from quiz.views.api.utils import CsrfExemptSessionAuthentication


bclient = brukva.Client()
bclient.connect()

@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([])
def submit(request):
    input_data = json.loads(request.body)
    is_true =  check_answer(input_data['message'])
    if is_true:
        input_data['message'] = input_data['message'] + get_answers()
    #print is_true
    #input_data['is_right']=check_answer(input_data['message'])
    input_data['is_right']=is_true
    input_data['is_service']=False
    #print input_data
    mess = {"action": "add_message", "data": input_data}
    #import pdb; pdb.set_trace()
    bclient.publish('common_chat', json.dumps(mess)) 
    m = ChatMessage()
    m.text = input_data['message']
    m.user = input_data['username']
    m.save()
    if is_true:
        thr = threading.Thread(target=swith_question_async,args=(1,))
        thr.start()
    return Response(
        { "status": 0 }
    )

@api_view(['GET'])
#@authentication_classes([])
#@permission_classes([])
def get_messages(request):

    mess = []
    for m in ChatMessage.objects.all().order_by('id')[0:40]:
        mess.append(
            {
                'username': m.user,
                'message': m.text,
                'is_right': m.is_right,
                'is_service': m.is_service
            }
        )
    mess.append(get_current_question())

    return Response(
        { "status": 0, 'data': mess }
    )


def swith_question_async(delay):
    time.sleep(delay)
    chat = ChatRoom.objects.first()
    chat.get_random_question()
    mess = {"action": "add_message", "data":get_current_question()}
    bclient.publish('common_chat', json.dumps(mess))
    

@api_view(['GET'])
#@authentication_classes([])
@permission_classes([])
def next_question(request):
    un = _(u'Master')
    med = _('Wait...Request for the next question.')
    message = {
        'is_right': False,
        'is_service': True,
        'username': '',
        'message': __('Wait...Request for the next question.')
    }
    mess = {"action": "add_message", "data": message}
    #import pdb; pdb.set_trace()
    bclient.publish('common_chat', json.dumps(mess))
    thr = threading.Thread(target=swith_question_async,args=(3,))
    thr.start()    
    return Response(
        { "status": 0 }
    )

