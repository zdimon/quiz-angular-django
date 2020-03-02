# -*- coding: utf-8 -*-
from .models import *
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext as __

def get_current_question():
    chat = ChatRoom.objects.first()
    q = ''
    if(chat.question.question_en):
        q = q+u'<strong><p>%s</p></strong>' % chat.question.question_en
    if(chat.question.question_ru):
        q = q+u'<strong><p>%s</p></strong>' % chat.question.question_ru
    un = _(u'Master')
    message = {
                'username': '',
                'question_ru': u'<strong><p>%s</p></strong>' % chat.question.question_ru,
                'question_en': u'<strong><p>%s</p></strong>' % chat.question.question_en,
                'is_right': 'alert',
                'is_service': True
            }
    return message

def check_answer(ans):
    chat = ChatRoom.objects.first()
    return chat.question.check_answer(ans)

def get_answers():
    chat = ChatRoom.objects.first()
    return '(<strong> %s  </strong>)' % ' | '.join([chat.question.answers_ru,chat.question.answers_en]) 