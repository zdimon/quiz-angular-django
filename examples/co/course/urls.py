from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
     url(r'^index/$', 'course.views.index', name='course'),
     url(r'^lesson/for/student/(?P<id>\d+).html$', 'course.views.lesson_for_student', name='lesson_for_student'),
     url(r'^lesson/for/owner/(?P<id>\d+).html$', 'course.views.lesson_for_owner', name='lesson_for_owner'),
     url(r'^owner/(?P<lesson_id>\d+).js$', 'course.views.js_for_owner', name='course_owner_js'),
     url(r'^student/(?P<lesson_id>\d+).js$', 'course.views.js_for_student', name='course_student_js'),
     url(r'^lesson/edit/(?P<id>\d+).js$', 'course.views.lesson_edit', name='lesson_edit'),
     url(r'^owner/(?P<lesson_id>\d+)_widget.js$', 'course.views.js_upload_image_widget', name='upload_image_widget'),
     url(r'^add/image$', 'course.views.add_image' , name="add-image"),
     url(r'^enter/(?P<email>[^\.]+)/(?P<token>[^\.]+)$', 'course.views.enter' , name="enter"),
     url(r'^subscribe/(?P<email>[^\.]+)/(?P<lesson_id>\d+)/(?P<token>[^\.]+)$', 'course.views.subscribe' , name="subscribe"),
     url(r'^clear/lesson/(?P<lesson_id>\d+)$', 'course.views.clear_lesson' , name="clear-lesson"),
     url(r'^detail/(?P<slug>[^\.]+).html$', 'course.views.detail', name='course_detail'),
     url(r'^add/me/to/course/(?P<course_id>\d+)$', 'course.views.add_me_to_course' , name="add-me-to-course"),
     url(r'^create/course$', 'course.views.create_course' , name="create-course"),
     url(r'^edit/course/(?P<course_id>\d+)$', 'course.views.edit_course' , name="edit-course"),
     url(r'^delete/course/(?P<course_id>\d+)$', 'course.views.delete_course' , name="delete-course"),
     url(r'^list/of/courses$', 'course.views.courses_list' , name="list-courses"),
     url(r'^create/lesson/(?P<course_id>\d+)$', 'course.views.create_lesson' , name="create-lesson"),
     url(r'^delete/lesson/(?P<lesson_id>\d+)$', 'course.views.delete_lesson' , name="delete-lesson"),
     url(r'^for_innerpage.js$', 'course.views.js_for_innerpage', name='js_for_innerpage'),
)




