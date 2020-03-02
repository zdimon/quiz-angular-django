from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
     url(r'^ajax/camera/on$', 'course.ajax.turn_owner_cam_on' , name="ajax-turn-owner-cam-on"),
     url(r'^ajax/camera/off$', 'course.ajax.turn_owner_cam_off' , name="ajax-turn-owner-cam-off"),
     url(r'^ajax/update/participants$', 'course.ajax.update_participants' , name="ajax-update-participants"),
     url(r'^ajax/show/camera$', 'course.ajax.show_owner_cam' , name="ajax-show-owner-cam"),
     url(r'^ajax/hide/camera$', 'course.ajax.hide_owner_cam' , name="ajax-hide-owner-cam"),
     url(r'^ajax/update/history$', 'course.ajax.update_history' , name="ajax-update-history"),
     url(r'^ajax/update/chat/messages$', 'course.ajax.update_chat_messages' , name="ajax-update-chat-messages"),
     url(r'^ajax/show/student/camera/(?P<type>[^\.]+)$', 'course.ajax.show_student_cam' , name="ajax-show-student-cam"),
     url(r'^ajax/hide/student/camera$', 'course.ajax.hide_student_cam' , name="ajax-hide-student-cam"),
     url(r'^ajax/delete/event$', 'course.ajax.delete_event' , name="delete-event"),
     url(r'^ajax/move/event/to/incubator$', 'course.ajax.move_event_to_incubator' , name="move-event-to-incubator"),
     url(r'^ajax/delete/incubator$', 'course.ajax.delete_incubator' , name="delete-event"),
     url(r'^ajax/move/incubator/to/event$', 'course.ajax.move_incubator_to_event' , name="move-incubator-to-event"),
     url(r'^ajax/incubator/fire$', 'course.ajax.incubator_fire' , name="incubator-fire"),
     url(r'^ajax/take/pic$', 'course.ajax.take_pic' , name="take-pic"),
     url(r'^ajax/save/pic$', 'course.ajax.save_pic' , name="save-pic"),
     url(r'^ajax/start/lesson$', 'course.ajax.start_lesson' , name="ajax-start-lesson"),
     url(r'^ajax/stop/lesson$', 'course.ajax.stop_lesson' , name="ajax-stop-lesson"),

     url(r'^ajax/alert/lesson/started$', 'course.ajax.alert_lesson_started' , name="ajax-alert-lesson-started"),
     url(r'^ajax/alert/lesson/stoped$', 'course.ajax.alert_lesson_stoped' , name="ajax-alert-lesson-stoped"),

     url(r'^ajax/gett/lesson/running$', 'course.ajax.get_lesson_running' , name="ajax-get-lesson-running"),

)




