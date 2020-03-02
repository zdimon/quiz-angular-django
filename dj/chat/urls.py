# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from .views import *


urlpatterns = [
    url(r'^submit$', submit),
    url(r'^get_messages$', get_messages),
    url(r'^next_question$', next_question)
]
