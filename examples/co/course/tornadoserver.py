# -*- coding: utf-8 -*-
"""
    Simple sockjs-tornado chat application. By default will listen on port 5555.
"""
import tornado.ioloop
import tornado.web
import time
import sockjs.tornado
import brukva
import json
import logging
from django.core.exceptions import ObjectDoesNotExist
c = brukva.Client()
c.connect()
logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
import os
from course.models import *
from course.tasks import *
from course.utils import *

class ChatConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    participants = set() # List of users online
    

    # Initialization
    def __init__(self,*args):
        super(ChatConnection, self).__init__(*args)
        self.client = brukva.Client()
        self.client.connect()
        self.user = None
        self.lesson = None
       

    # When connection need to be open
    def on_open(self, info):
        ''' function when someone made connection from javascript'''
        # Send that someone joined
        message = {"act" : "someone_joined", "content" : "Someone joined"}
        self.broadcast(self.participants, json.dumps(message))
        # Add client to the clients list
        self.participants.add(self)

    # When we recieve message from redis server we go here
    def redis_message(self, result):
        ''' recieving  message from redis server, 
            convertin it in json format 
            and sending it to the current chanel
        '''
        message = json.loads(result.body)
        self.send(json.dumps(message))

    # Subscribe user to channel
    def subscribe(self, room):
        self.client.subscribe(room) # Redis subscribe
        logger.debug('subscribing to room %s' % (room, )) # Debug
        self.client.listen(self.redis_message)

    # When we receive messages we go here
    def on_message(self, message): 
        ''' handler of message '''
        logger.debug(message) # Debug
        message = json.loads(message)
        # When we open connection
        if message['act'] == 'open_connect':
            logger.debug('Connection esteblished.')
            self.user = UserProfile.objects.get(pk=message['user_id'])
            self.lesson = Lesson.objects.get(pk=message['lesson_id'])
            add_user_if_not_exist(self.user, self.lesson)
            mes = { 'act': 'somebody_joined', 'message': 'Someone joined' }  
            self.broadcast(self.participants, json.dumps(mes))
            mes = { 'act': 'update_participants'}  
            self.broadcast(self.participants, json.dumps(mes))
            self.subscribe('lesson_%s_%s' % (message['lesson_id'], message['user_id']))
        if message['act'] == 'open_connect_innerpage':
            logger.debug('Connection esteblished from innerpage.')
            self.subscribe('innerpage_%s' %  message['user_id'])
        if message['act'] == 'ping':
            mes = { 'act': 'pong', 'message': message['message'] }  
            self.broadcast(self.participants, json.dumps(mes))
        if message['act'] == 'owner_turn_cam_on':
            mes = { 'act': 'turn_owner_cam_on', 'message': message['lesson_id'] }  
            c.publish('lesson_%s_%s' % (message['lesson_id'], message['user_id']), json.dumps(mes)) 
            logger.debug('User turn his cam on in %s lesson' % (message['lesson_id'], ))
        if message['act'] == 'turn_owner_cam_off':
            mes = { 'act': 'turn_owner_cam_off', 'message': message['message'] }  
            self.broadcast(self.participants, json.dumps(mes))
        if message['act'] == 'clear_writeboard':
            logger.debug('Clearing writeboard %s' % message['lesson_id'])
            mes = { 'act': 'clear_writeboard' }  
            c.publish('lesson_%s_%s' % (message['lesson_id'], message['user_id']), json.dumps(mes))  
        if message['act'] == 'text_message': 
            if message['replace'] =='yes':
                mes = { 'act': 'clear_writeboard' } 
                c.publish('lesson_%s_%s' % (message['lesson_id'], message['user_id']), json.dumps(mes)) 
            mes =  message['content']
            mes = mes.replace('&',u'&amp;')
            mes = mes.replace('<',u'&lt;')
            mes = mes.replace('>',u'&gt;')
            
            
            logger.debug('Text message %s to %s lesson' % (message['content'], message['lesson_id']))
            mes = { 'act': 'text_message', 'message':  mes, 'text_size': message['text_size'], 'text_color': message['text_color'], 'text_align': message['text_align'] }  
            c.publish('lesson_%s_%s' % (message['lesson_id'], message['user_id']), json.dumps(mes)) 
        if message['act'] == 'chat_message': 
            logger.debug('Text chat message %s to %s lesson' % (message['content'], message['lesson_id']))
            mes = { 'act': 'chat_message', 'message':  message['content'], 'avatar': message['avatar'], 'user_name': message['user_name']}  
            c.publish('lesson_%s_%s' % (message['lesson_id'], message['user_id']), json.dumps(mes)) 
        if message['act'] == 'send_image': 
            if message['replace'] =='yes':
              mes = { 'act': 'clear_writeboard' }  
              c.publish('lesson_%s_%s' % (message['lesson_id'], message['user_id']), json.dumps(mes)) 
            logger.debug('Sending image %s to %s lesson' % (message['image_path'], message['lesson_id']))
            image = "<img class='from_publisher' src='%s'>" % ( message['image_path'],)    
            mes = { 'act': 'text_message', 'message':  image}  
            c.publish('lesson_%s_%s' % (message['lesson_id'], message['user_id']), json.dumps(mes)) 
            
        if message['act'] == 'save_event': 
            try:
                text_size = message['text_size']
                text_color = message['text_color']
                text_align = message['text_align']
            except:
                text_size = 0
                text_color = 0
                text_align = 0

            save_event.delay(self.user,message['message'],message['type'],self.lesson, text_size, text_color, text_align)
        if message['act'] == 'save_chat_message': 
            save_chat_message.delay(self.user,message['message'],self.lesson)
        if message['act'] == 'turn_student_camera': 
            logger.debug('Turn student cam in %s' % (message['user_id'],))
            mes = { 'act': 'turn_student_cam_on', 'user_id':  message['user_id']}  
            c.publish('lesson_%s_%s' % (message['lesson_id'], message['user_id']), json.dumps(mes)) 
        if message['act'] == 'turn_student_cam_out': 
            logger.debug('Turn student cam out %s student id %s' % (message['user_id'],message['student_id']))
            mes = { 'act': 'turn_student_cam_out_on', 'user_id':  message['user_id'], 'student_id': message['student_id']}  
            c.publish('lesson_%s_%s' % (message['lesson_id'], message['user_id']), json.dumps(mes)) 
        if message['act'] == 'turn_student_cam_off': 
            logger.debug('Turn student cam off %s' % (message['user_id'],))
            mes = { 'act': 'turn_student_cam_off', 'user_id':  message['user_id'], 'token': message['token']}  
            c.publish('lesson_%s_%s' % (message['lesson_id'], message['user_id']), json.dumps(mes)) 

        if message['act'] == 'turn_student_mic_on': 
            logger.debug('Turn student mic on %s' % (message['user_id'],))
            mes = { 'act': 'turn_student_mic_on', 'user_id':  message['user_id'], 'token': message['token']}  
            c.publish('lesson_%s_%s' % (message['lesson_id'], message['user_id']), json.dumps(mes)) 

        if message['act'] == 'turn_student_mic_off': 
            logger.debug('Turn student mic off %s' % (message['user_id'],))
            mes = { 'act': 'turn_student_mic_off', 'user_id':  message['user_id'], 'token': message['token']}  
            c.publish('lesson_%s_%s' % (message['lesson_id'], message['user_id']), json.dumps(mes)) 


            #self.broadcast(self.participants, json.dumps(mes))
    # When current user tries to disconnect
    def on_close(self):
        self.participants.remove(self)
        Users2Lesson.objects.filter(user=self.user).delete()
        mes = { 'act': 'update_participants'}  
        self.broadcast(self.participants, json.dumps(mes))
        logger.debug('User left')        


    def redis_message(self, result):
        ''' recieving  message from redis server, 
            convertin it in json format 
            and sending it to the current chanel
        '''
        message = json.loads(result.body)
        self.send(json.dumps(message))

        # Subscribe user to channel
    def subscribe(self, room):
        self.client.subscribe(room) # Redis subscribe
        logger.debug('subscribing to room %s' % (room, )) # Debug
        self.client.listen(self.redis_message)

