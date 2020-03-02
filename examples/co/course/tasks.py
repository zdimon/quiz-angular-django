# -*- coding: utf-8 -*-
from celery import task
from celery.utils.log import get_task_logger
import time
from course.models import *


logger = get_task_logger(__name__)
logger.setLevel('DEBUG')

@task(name='save_event')
def save_event(user, message, type, lesson, text_size, text_color, text_align):
    logger.info('Save message...')
    e = Event()
    e.tp = type
    e.text = message
    e.lesson = lesson
    e.text_size = text_size
    e.text_color = text_color
    e.text_align = text_align
    e.save()

@task(name='save_chat_message')
def save_chat_message(user, message, lesson):
    logger.info('Save chat message...')
    m = ChatMessages()
    m.text = message
    m.lesson = lesson
    m.user = user
    m.save()

