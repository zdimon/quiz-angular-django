# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns( '',
    url(r'^result$', 'liqpay.views.result'),
    url(r'^server$', 'liqpay.views.server'),
   )