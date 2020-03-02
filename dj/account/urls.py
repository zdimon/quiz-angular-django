# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers
from .views import *
from .api import login, logout, reg, get_token_from_session


urlpatterns = [
    url(r'^$', show),
    url(r'^check/session$', check_session),
    url(r'^save/pic$', save_pic),
    url(r'^register/$', MyRegistrationView.as_view(), name='register'),
    url(r'^profile/edit$', ProfileEditView.as_view(), name='profile_edit'),
    url(r'^registration/done', registration_done, name='registration_done'),
    url(r'^activation/done', activation_done, name='activation_done'),
    url(r'^activate/(?P<activation_key>[-:\w]+)/$', MyActivationView.as_view(),name='registration_activate'),
    
]

### API

from rest_framework import routers
#from .views import *
#router = routers.SimpleRouter()
#router.register(r'users', UserViewSet)

urlpatterns = urlpatterns + [

    url(r'^session/token$', get_token_from_session),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^reg/$', reg),
]