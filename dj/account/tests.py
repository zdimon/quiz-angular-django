# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import requests
import json
from django.contrib.auth.models import User
from .api import *


from utils.api_client import Client
client = Client()

try:
    from dj.settings import TEST_URL
except:
    raise Exception('Please set the TEST_URL in local.py for example "http://localhost:8080"')

class LoginLogoutCase(TestCase):
    def setUp(self):
        # создадим тестового юзера
        self.client = Client()
        try:
            p = User()
            p.username = 'test'
            p.set_password('pwd')
            p.is_active = True
            p.save()
            User.objects.create_user(username='testuser', password='12345')
        except Exception as e:
            print str(e)
        #Animal.objects.create(name="cat", sound="meow")

    def test_login(self):
        print 'Login'

        out = client.post('/api/v1/account/login/',{ 'username': 'test', 'password': 'pwd' })
        self.assertEqual(out['status_code'],200)
        self.assertEqual(out['status'],0)
        #self.logout(113)


        out = client.post('/api/v1/account/login/',{ 'username': '1qw2e3qwdqwrf', 'password': 'pwd' })
        self.assertEqual(out['status'],1)


    def test_logout(self):
        print 'Logout '
        user = User.objects.get(username='testuser')
        rez = client.get('/api/v1/account/logout/',logout,user)
        self.assertEqual(rez['status'],0)
       

    def test_registration(self):
        print 'Registration '
        data = { 'email': 'tratra@ddd.dd', 'password': '123' } 
        rez = client.post('/api/v1/account/reg/',data)
        print rez
        self.assertEqual(rez['status'],0)
