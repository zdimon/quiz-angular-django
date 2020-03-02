# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from registration.models import RegistrationProfile
from registration import signals


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([])
def get_token_from_session(request):
    if not request.user.is_authenticated():
        return Response({
            'status': 1,
            'message': 'User is not authenticated!'
        })
    user = request.user
    
    try:
        t = Token.objects.get(user=user) 
    except:
        t = Token.objects.create(user=user)
    return Response({
        'status': 0,
        'token': t.key
    })

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login(request):
    """
    Запрос логина.

    **Данные**

        {"username": str, "password": str}

    **Ответ.**

        {status: 0, 'message': str, 'user_id': int, 'token': token}

    """
    input_data = json.loads(request.body)
    
    try:
        #import pdb; pdb.set_trace()
        user = User.objects.get(username=input_data['username'])
        if user.check_password(input_data['password']):
            # генерим токен или получаем
            try:
                t = Token.objects.get(user=user)
            except:
                t = Token.objects.create(user=user)
            out = {"status": 0, 'user_id': user.id, 'token': t.key}
        else:
            out = {"status": 1, "message": "Password is invalid."}
    except:
        out = {"status": 1, "message": "Login is invalid."}

    print out
    return Response(out)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def reg(request):
    """
    Запрос регистрации.
    :email
    :password
    **Ответ.**

        {status: 0, 'message': str, 'user_id': int, 'token': token}

    """
    input_data = json.loads(request.body)
    p = User()
    p.username = input_data['email']
    p.email = input_data['email']
    p.set_password(input_data['password'])
    p.is_active = True
    p.save()
    RegistrationProfile.objects.create_profile(p)

    signals.user_registered.send(sender='API',
                                    user=p,
                                    request=request)
    t = Token.objects.get(user=p)

    data = {'status': 0, 'user_id': p.id, 'token': t.key}
    return Response(data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def logout(request):
    content = {
        'status': 0,  
        'message': 'ok'
    }
    return Response(content)