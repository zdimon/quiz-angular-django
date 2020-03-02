from django.shortcuts import render
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from main.forms import ProfileForm
from main.models import UserProfile
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from course.models import Lesson
from co.settings import SOCKJS_SERVER
from django.core.urlresolvers import reverse
from course.utils import *
from course.forms import ImageForm, AjaxImageForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import brukva
bclient = brukva.Client()
bclient.connect()
from django.contrib.auth.models import User
from django.contrib import messages
from course.models import *
from course.forms import *
from django.utils.translation import ugettext as _
from co.settings import VIDEO_SERVER


# Create your views here.
@login_required
def index(request):
    lessons = Lesson.objects.all().filter(is_active=True)
    context = {'lessons': lessons}
    return render_to_response('index.html', context, RequestContext(request))

@login_required
def lesson_for_student(request,id):
    lesson = Lesson.objects.get(pk=id)
    
    context = {'lesson': lesson, 'video_server': VIDEO_SERVER}
    return render_to_response('lesson_for_student.html', context, RequestContext(request))

@login_required
def lesson_for_owner(request,id):
    lesson = Lesson.objects.get(pk=id)
    incubator = Incubator.objects.filter(lesson=lesson).order_by('sorting')
    context = {'incubator': incubator, 'lesson': lesson, 'form': AjaxImageForm(), 'user': request.user, 'video_server': VIDEO_SERVER}
    return render_to_response('lesson_for_owner.html', context, RequestContext(request))



def js_for_owner(request,lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    context = {'server': SOCKJS_SERVER, 'lesson': lesson}
    return render_to_response('course_for_owner.js', context, RequestContext(request))


def js_for_student(request,lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    context = {'server': SOCKJS_SERVER, 'lesson': lesson}
    return render_to_response('course_for_student.js', context, RequestContext(request))


def js_for_innerpage(request):
    context = {'server': SOCKJS_SERVER}
    return render_to_response('course_for_innerpage.js', context, RequestContext(request))


def js_upload_image_widget(request,lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    context = {'server': SOCKJS_SERVER, 'lesson': lesson}
    return render_to_response('upload_widget.js', context, RequestContext(request))


from django import forms
from ajax_upload.widgets import AjaxClearableFileInput

class MyForm(forms.Form):
    my_image_field = forms.ImageField(widget=AjaxClearableFileInput())


@login_required
def lesson_edit(request,id):
    lesson = Lesson.objects.get(pk=id)
    events = Event.objects.filter(lesson=lesson).order_by('-id')
    incubators = Incubator.objects.filter(lesson=lesson).order_by('-id')
    if request.method == 'POST':
        form_lesson = LessonForm(request.POST, request.FILES, instance=lesson)
        if form_lesson.is_valid():
            form_lesson.save()
        messages.add_message(request, messages.INFO, _('Lesson was saved!'))
        return redirect('lesson_edit', id=lesson.pk)
        #return redirect(reverse('lesson_edit', args=[lesson.id]))
    else:
        form_lesson = LessonForm(instance=lesson)
    if request.method == 'POST':
        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('lesson_edit', args=[lesson.id]))
    else:
        form = ImageForm()

    context = {'lesson': lesson, 'form_lesson': form_lesson, 'form': form, 'events': events, 'incubators': incubators}
    return render_to_response('lesson_edit.html', context, RequestContext(request))



@csrf_exempt
def add_image(request):
    from course.forms import ImportImageForm
    #import pdb; pdb.set_trace()
    if request.method == 'POST':
        form = ImportImageForm(request.POST, request.FILES)
        if form.is_valid():
            im = form.save()
            lesson = im.lesson
            mes = { 'act': 'add_image_from_publisher', 'image_id': im.id, 'image': im.link, 'publish': im.publish}
            r = 'lesson_%s_%s' % (lesson.id, lesson.owner.id)
            bclient.publish(r, json.dumps(mes))            
    else:
        form = ImportImageForm()
    return render_to_response('image_add.html', {'form':form},context_instance=RequestContext(request))


@csrf_exempt
def enter(request,email,token):
    from django.shortcuts import redirect
    from django.contrib.auth import authenticate, login
    from django.http import HttpResponseRedirect
    uname = email.replace('--att--','@')
    uname = uname.replace('--dot--','.')
    try:
        user = User.objects.get(username=uname)
    except:
        user = UserProfile()
        user.username = uname
        user.set_password('123')
        user.is_active = True
        user.email = uname
        user.save()
        user = User.objects.get(username=uname)
    user.backend = 'main.auth.ProfileUserModelBackend'
    login(request, user)
    return redirect('lesson_for_student', id=1)

# http://localhost:8888/course/subscribe/b--att--a--dot--a/1/bla
def subscribe(request,email,lesson_id,token):
    from django.shortcuts import redirect
    from django.contrib.auth import authenticate, login
    from django.http import HttpResponseRedirect
    uname = email.replace('--att--','@')
    uname = uname.replace('--dot--','.')
    lesson = Lesson.objects.get(pk=lesson_id)
    try:
        user = UserProfile.objects.get(username=uname)
    except:
        user = UserProfile()
        user.username = uname
        user.set_password('123')
        user.is_active = True
        user.email = uname
        user.save()
        
    user.backend = 'main.auth.ProfileUserModelBackend'
    login(request, user)
    try:
        Subscriber2Lesson.objects.get(lesson=lesson, user=user)
    except:
        u2l = Subscriber2Lesson()
        u2l.user = user
        u2l.lesson = lesson
        u2l.save()

    return redirect('my_profile')


@login_required
def clear_lesson(request,lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    messages.add_message(request, messages.INFO, 'Lesson was cleaned.')
    lesson.clear()
    return redirect('my_profile')


@login_required
def detail(request,slug):
    course = Course.objects.get(name_slug=slug)
    context = {'course': course}
    return render_to_response('course_detail.html', context, RequestContext(request))


@login_required
def add_me_to_course(request,course_id):
    course = Course.objects.get(pk=course_id) 
    try:
        u2c = Users2Course.objects.get(user=request.user, course=course)
        messages.add_message(request, messages.ERROR, _('You are already subscribed.'))
    except:
        u2c = Users2Course()
        u2c.user = request.user
        u2c.course = course
        u2c.save()
        for l in Lesson.objects.filter(course=course):
            u2l = Subscriber2Lesson()
            u2l.user = request.user
            u2l.lesson = l
            u2l.save()
        messages.add_message(request, messages.INFO, _('You was subscribed successfully.'))
    return redirect('my_profile')



@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            i = form.save()
        return redirect('edit-course', course_id=i.pk)
    else:
        course = Course()
        course.owner = request.user
        form = CourseForm(instance=course)
    context = {'form': form}
    return render_to_response('create_course.html', context, RequestContext(request))

@login_required
def edit_course(request,course_id):
    course = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            i = form.save()
        messages.add_message(request, messages.INFO, _('New course was created!'))
        return redirect('edit-course', course_id=i.pk)
    else:
        form = CourseForm(instance=course)
    context = {'form': form}
    return render_to_response('edit_course.html', context, RequestContext(request))


@login_required
def delete_course(request,course_id):
    course = Course.objects.get(pk=course_id)
    if course.owner == request.user:
        messages.add_message(request, messages.INFO, _('Course was deleted!'))
        course.delete()
    return redirect('list-courses')



@login_required
def courses_list(request):
    courses = Course.objects.filter(owner=request.user).all()
    context = {'courses': courses}
    return render_to_response('courses_list.html', context, RequestContext(request))


@login_required
def create_lesson(request,course_id):
    course = Course.objects.get(pk=course_id)
    lesson = Lesson()
    lesson.owner = request.user
    lesson.course = course
    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            l = form.save()
        #return redirect('edit-lesson', lesson_id=i.pk)
        messages.add_message(request, messages.INFO, _('New lesson was created!'))
        return redirect('list-courses')
    else:
        form = LessonForm(instance=lesson)
    context = {'course': course, 'form': form}
    return render_to_response('create_lesson.html', context, RequestContext(request))




@login_required
def delete_lesson(request,lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    if lesson.owner == request.user:
        messages.add_message(request, messages.INFO, _('Lesson was deleted!'))
        lesson.delete()
    return redirect('list-courses')



