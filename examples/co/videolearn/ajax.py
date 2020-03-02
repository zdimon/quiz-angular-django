from django_ajax.decorators import ajax
import pickle   
from django.utils.translation import ugettext as _
import json
import logging
import time
from django.template import loader, Context    
from videolearn.models import Vcourse, Vlesson, Access
from liqpay.models import Liqpay
from videolearn.models import gidrate_lessons

def test_show_template():
    t = loader.get_template('test_show.html')
    c = Context({})
    return t.render(c)


def course_list_template(request):
    courses = Vcourse.objects.filter(owner=request.user)
    t = loader.get_template('a_course_list.html')
    c = Context({'courses': courses })
    return t.render(c)


def material_list_template(request):
    bb = Liqpay.objects.filter(user=request.user, is_success=True)
    materials = []
    for b in bb:
        materials.append(b.lesson)
    materials = gidrate_lessons(materials,request.user)
    t = loader.get_template('a_material_list.html')
    c = Context({ 'lessons': materials })
    return t.render(c)



@ajax
def test_show(request):
    data = {
            'fragments': { 
                '#show_test_div': test_show_template(),
                
             },   

            
                
           }
    return data    



@ajax
def course_list(request):
    data = {
            'fragments': { 
                '#left_course': course_list_template(request),
                
             },        
                
           }
    return data


@ajax
def material_list(request):
    data = {
            'fragments': { 
                '#left_material': material_list_template(request),
                
             },        
                
           }
    return data



