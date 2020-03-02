from django.conf.urls import patterns, url
from videolearn.views import *
from videolearn.ajax import *

urlpatterns = patterns('',
    url(r'^test$', test ),
    url(r'^course/new$', edit_course, {}, name='create-vcourse'),
    url(r'^course/edit/(?P<id>\d+)/$', edit_course, {}, 'edit-vcourse'),
    url(r'^course/delete/(?P<id>\d+)/$', delete_course, {}, 'delete-vcourse'),
    url(r'^course/list$', list_courses, name='list-vcourse'),
    url(r'^lecture/new/(?P<course_id>\d+)$', edit_lecture, {}, name='add-lecture'),
    url(r'^lecture/edit/(?P<id>\d+)/(?P<course_id>\d+)$', edit_lecture, {}, 'edit-lecture'),
    url(r'^lecture/delete/(?P<lecture_id>\d+)$', delete_lecture, {}, 'delete-lecture'),
    url(r'^lecture/start/(?P<id>\d+)$', start_lecture, {}, name='start-lecture'),
    url(r'^detail/(?P<slug>[^\.]+).html$', detail, name='vcourse-detail'),
    url(r'^lecture/preview/(?P<id>\d+)$', preview, name='vcourse-preview'),
    url(r'^lecture/show/(?P<id>\d+)$', show, name='vcourse-show'),
    url(r'^lecture/buy/(?P<id>\d+)$', buy, name='vcourse-buy'),
    url(r'^lecture/testbuy/(?P<id>\d+)$', testbuy, name='test-buy'),
    url(r'^library/$', library, name='library-vcourse'),

    url(r'^article/new/(?P<lesson_id>\d+)$', edit_article, {}, name='add-article'),
    url(r'^article/edit/(?P<id>\d+)/(?P<lesson_id>\d+)$', edit_article, {}, name='edit-article'),
    url(r'^article/show/(?P<id>\d+)$', show_article, {}, name='article-detail'),

    ## AJAX
    url(r'^ajax/test_show$', test_show ),
    url(r'^ajax/course-list$', course_list, name='course-list'),
    url(r'^ajax/material-list$', material_list, name='material-list'),

)
