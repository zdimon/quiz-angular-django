"""dj1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from main.views import index, ping, cert, change_language
from django.contrib.auth import views as auth_views
from account.views import MyLoginView
from django.conf.urls.i18n import i18n_patterns
from main.views import socket_online, user_online
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^socket_online/', socket_online),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^user_online/', user_online),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^rosetta/', include('rosetta.urls')),
    url(r'^change_language/', change_language, name='change_language'), 
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^.well-known/acme-challenge/hLcZHCBseQmkFYXNilEpAaJFJM3LF63pUEhEkTABgdM', cert),
    url('admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'), 

    url(r'^api/v1/account/', include('account.urls')),
    

]

urlpatterns += i18n_patterns(
   url(r'^chat/', include('chat.urls')),
   url(r'^$', index, name="mainpage"),
   url(r'^quiz/', include('quiz.urls', namespace='quiz')),
   url(r'^user/', include('account.urls')),
   url(r'^accounts/login/$', MyLoginView.as_view(), name='login'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
)

urlpatterns = urlpatterns+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
