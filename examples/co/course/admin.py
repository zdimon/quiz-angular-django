from django.contrib import admin
from image_cropping import ImageCroppingMixin
# Register your models here.

from course.models import *

class CourseAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ("thumb", "name", "is_active")


class LessonAdmin(admin.ModelAdmin):
    list_display = ("name", "thumb", "is_active", "start_at")

class TopicAdmin(admin.ModelAdmin):
    pass

class EventAdmin(admin.ModelAdmin):
    list_display = ("text", "tp", "created")


class ImagesAdmin(admin.ModelAdmin):
    list_display = ("image","lesson", "created")


class ChatMessagesAdmin(admin.ModelAdmin):
    list_display = ("user","text", "lesson", "created")

admin.site.register(ChatMessages, ChatMessagesAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Images, ImagesAdmin)


