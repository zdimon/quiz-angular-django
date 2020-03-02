# -*- coding: utf-8 -*-
from django.shortcuts import render
from videolearn.forms import *
from videolearn.models import Vcourse, Vlesson, Access, Varticles
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import loader, RequestContext
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from co.settings import VIDEO_SERVER
from co.settings import LIQPAY_PRIVATE_KEY, LIQPAY_PUBLIC_KEY, LIQPAY_RESULT_URL, LIQPAY_SERVER_URL
from liqpay.liqpay import LiqPay
from videolearn.models import gidrate_lessons
from liqpay.models import Liqpay

def test(request):
    context = {'server': VIDEO_SERVER}
    return render_to_response('test.html', context, RequestContext(request))


@login_required
def library(request):
    lp = Liqpay.objects.filter(user=request.user,is_success=True)
    lessons = []
    for p in lp:
        lessons.append(p.lesson)
    lessons = gidrate_lessons(lessons,request.user)
    context = {'lessons': lessons}
    return render_to_response('library.html', context, RequestContext(request))



@login_required
def buy(request,id):
    lesson = get_object_or_404(Vlesson, pk=id)
    l = Liqpay()
    l.user = request.user
    l.lesson = lesson
    l.amount = lesson.price
    l.save()
    liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
    form = liqpay.cnb_form({"amount" : lesson.price,
                            "currency" : "UAH",
                            "description" : u"Покупка видеоурока",
                            "order_id" : l.id,
                            "result_url": LIQPAY_RESULT_URL,
                            "server_url": LIQPAY_SERVER_URL,
                            "type" : "buy",
                            "sandbox" : "1"})
    context = {'lesson': lesson, 'button': form}
    return render_to_response('buy.html', context, RequestContext(request))



@login_required
def testbuy(request,id):
    lesson = get_object_or_404(Vlesson, pk=id)
    l = Liqpay()
    l.user = request.user
    l.lesson = lesson
    l.amount = lesson.price
    l.is_success = True
    l.save()
    liqpay = LiqPay(LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY)
    form = liqpay.cnb_form({"amount" : lesson.price,
                            "currency" : "UAH",
                            "description" : u"Покупка видеоурока",
                            "order_id" : l.id,
                            "result_url": LIQPAY_RESULT_URL,
                            "server_url": LIQPAY_SERVER_URL,
                            "type" : "buy",
                            "sandbox" : "1"})
    context = {'lesson': lesson, 'button': form}
    return render_to_response('buy.html', context, RequestContext(request))


@login_required
def preview(request,id):
    lesson = get_object_or_404(Vlesson, pk=id)
    if lesson.owner!=request.user:
        return HttpResponseForbidden()
    context = {'server': VIDEO_SERVER, 'lesson': lesson}
    return render_to_response('preview.html', context, RequestContext(request))


@login_required
def show(request,id):
    lesson = get_object_or_404(Vlesson, pk=id)
    
    if lesson.course.type=='v':
        tpl = 'show_video.html'
    else:
        tpl = 'show_audio.html'
    if lesson.price>0:
        try:
            Liqpay.objects.get(user=request.user,is_success=True,lesson=lesson)
        except:
            tpl = 'forbidden.html'
    '''
    try:
        a = Access.objects.get(user=request.user,lesson=lesson)
    except:
        a = Access()
        a.user = request.user
        a.lesson = lesson
        a.save()
    '''
    context = {'server': VIDEO_SERVER, 'lesson': lesson}

    return render_to_response(tpl, context, RequestContext(request))



@login_required
def edit_course(request,id=None):

    if id:
        course = get_object_or_404(Vcourse, pk=id)
        #if article.author != request.user:
        #    return HttpResponseForbidden()
    else:
        course = Vcourse(owner=request.user)

    if request.POST:
        form = VcourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Course has been saved!'))
    else:
        form = VcourseForm(instance=course)

    context = {'form': form}
    return render_to_response('edit_vcourse.html', context, RequestContext(request))




@login_required
def edit_lecture(request,id=None,course_id=None):
    course = get_object_or_404(Vcourse, pk=course_id)
    if id:
        lecture = get_object_or_404(Vlesson, pk=id)
        
        #if article.author != request.user:
        #    return HttpResponseForbidden()
    else:
        lecture = Vlesson(owner=request.user,course=course, price=course.price)

    if request.POST:
        form = VlessonForm(request.POST, request.FILES, instance=lecture)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Lecture has been saved!'))
            return redirect('cabinet')
    else:
        form = VlessonForm(instance=lecture)

    context = {'form': form}
    return render_to_response('edit_vlesson.html', context, RequestContext(request))


@login_required
def start_lecture(request,id=None):
    l = get_object_or_404(Vlesson, pk=id)
    art = Varticles.objects.filter(lesson=l).order_by('id')
    return redirect('article-detail', id=art[0].id)


@login_required
def delete_lecture(request,lecture_id):
    lesson = get_object_or_404(Vlesson, pk=lecture_id)
    if lesson.owner == request.user:
        lesson.delete()
        messages.add_message(request, messages.INFO, _('Lesson deleted!'))
    else:
        messages.add_message(request, messages.ERROR, _('Error!'))
    
    return redirect('cabinet')



@login_required
def edit_article(request,id=None, lesson_id=None):
    print 'dddddd %s' % lesson_id
    lesson = get_object_or_404(Vlesson, pk=lesson_id)
    if id:
        
        article = get_object_or_404(Varticles, pk=id)
        
        #if article.author != request.user:
        #    return HttpResponseForbidden()
    else:
        article = Varticles(owner=request.user,lesson=lesson)

    if request.POST:
        form = VarticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, _('Article has been saved!'))
            return redirect('cabinet')
    else:
        form = VarticleForm(instance=article)

    context = {'form': form}
    return render_to_response('edit_varticle.html', context, RequestContext(request))


#@login_required
def show_article(request,id=None):
    article = get_object_or_404(Varticles, pk=id)
    lesson = article.lesson
    articles = Varticles.objects.filter(lesson=lesson).order_by('id')
    tpl = 'show_varticle.html'
    #import pdb; pdb.set_trace()
    if lesson.price>0 and article.is_free == False:
        try:
            Liqpay.objects.get(user=request.user,is_success=True,lesson=lesson)
        except:
            tpl = 'forbidden.html'
    context = {'article': article, 'articles': articles, 'lesson': lesson}
    return render_to_response(tpl, context, RequestContext(request))

@login_required
def delete_course(request,id):
    course = get_object_or_404(Vcourse, pk=id)
    if course.owner == request.user:
        course.on_delete = True
        course.save()
    else:
        messages.add_message(request, messages.ERROR, _('Error!'))
    messages.add_message(request, messages.INFO, _('Course has been mark for deleting!'))
    return redirect('list-vcourse')


@login_required
def list_courses(request,id=None):
    courses = Vcourse.objects.filter(owner=request.user)
    context = {'courses': courses}
    return render_to_response('list_vcourse.html', context, RequestContext(request))



def detail(request,slug):
    
    course = get_object_or_404(Vcourse, name_slug=slug)
    lessons = Vlesson.objects.filter(course=course, is_converted=True, is_public=True)
    lessons = gidrate_lessons(lessons,request.user)
    context = {'course': course, 'lessons': lessons}
    return render_to_response('vcourse_detail.html', context, RequestContext(request))


