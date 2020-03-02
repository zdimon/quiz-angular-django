# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.
class ChatRoom(models.Model):
    '''
        Chat room
    '''
    from quiz.models.models import Question
    question = models.ForeignKey(Question, verbose_name=_(u'Question'))
    timer = models.IntegerField()

    def get_random_question(self):
        from quiz.models.models import Question
        q = Question.objects.filter(lang='ru-en').order_by('?').first()
        self.question = q
        self.save()


class ChatMessage(models.Model):
    '''
        Chat messages
    '''
    is_right = models.BooleanField(default=False)
    is_service = models.BooleanField(default=False)
    text = models.TextField(verbose_name=_(u'Text'))
    user = models.CharField(verbose_name=_(u'User'), max_length= 250)
    created_at = models.DateTimeField(auto_now_add=True)