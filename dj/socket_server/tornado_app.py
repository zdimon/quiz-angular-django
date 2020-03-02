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


class QuizConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    participants = set() # List of users online
    

    # Initialization
    def __init__(self,*args):
        super(QuizConnection, self).__init__(*args)
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

    # When we receive messages we go here
    def on_message(self, message): 
        ''' handler of message '''
        logger.debug(message) # Debug
        message = json.loads(message)
        # When we open connection
        if message['action'] == 'open_connect':
            logger.debug('Connection esteblished.')
            mes = { 'action': 'somebody_joined', 'message': 'Someone joined' }  
            self.broadcast(self.participants, json.dumps(mes))
            
       

            #self.broadcast(self.participants, json.dumps(mes))
    # When current user tries to disconnect
    def on_close(self):
        self.participants.remove(self)
        Users2Lesson.objects.filter(user=self.user).delete()
        mes = { 'act': 'update_participants'}  
        self.broadcast(self.participants, json.dumps(mes))
        logger.debug('User left')        



        # Subscribe user to channel
    def subscribe(self, room):
        self.client.subscribe(room) # Redis subscribe
        logger.debug('subscribing to room %s' % (room, )) # Debug
        self.client.listen(self.redis_message)

