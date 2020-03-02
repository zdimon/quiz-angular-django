# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import ChatRoom, ChatMessage

# Register your models here.

class ChatRoomAdmin(admin.ModelAdmin):
    #pass
    list_display = ('question',)
admin.site.register(ChatRoom, ChatRoomAdmin)


class ChatMessageAdmin(admin.ModelAdmin):
    #pass
    list_display = ('text', 'user', 'created_at')
admin.site.register(ChatMessage, ChatMessageAdmin)