from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'main.views.home', name='home'),
     url(r'^rosetta/', include('rosetta.urls')),
     url(r'^course/', include('course.ajax_urls')),
     url(r'', include('social_auth.urls')),
     url(r'^admin/', include(admin.site.urls)),
     url(r'^ckeditor/', include('ckeditor.urls')),
     url(r'^videolearn/', include('videolearn.urls')),
     url(r'^liqpay/', include('liqpay.urls')),
     url(r'^redactor/', include('redactor.urls')),
)

urlpatterns += i18n_patterns('',
     url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/'}, name='logout'),
     url(r'^course/', include('course.urls')),
     url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
     url(r'^accounts/profile/$', 'main.views.cabinet', name='my_profile'),
     url(r'^cabinet/$', 'main.views.cabinet', name='cabinet'),
     url(r'^edit/profile/$', 'main.views.profile', name='edit_profile'),
     url(r'^accounts/', include('registration.backends.default.urls')),
     
     url(r'^grappelli/', include('grappelli.urls')), 
     url(r'^$', include('django.contrib.flatpages.urls')),
     url(r'^ajax-upload/', include('ajax_upload.urls')),
     
     
     url(r'^change_language/', 'main.views.change_language', name='change_language'),
     url(r'^lesson/edit/(?P<id>[^\.]+).html', 'course.views.lesson_edit', name="lesson-edit"),


     
)


from django.conf import settings
from django.conf.urls.static import static
urlpatterns += [
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

