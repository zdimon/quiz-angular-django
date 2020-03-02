# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from main.forms import ProfileForm
from main.models import UserProfile
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from course.models import *
from django.contrib.flatpages.models import FlatPage
from course.models import Course
from videolearn.models import Vcourse


# Create your views here.
def home(request):
    try:
        page = FlatPage.objects.get(pk=1)
    except:
        page = None
    courses = Course.objects.filter(is_active=True)
    vcourses = Vcourse.objects.filter(is_active=True)
    users = UserProfile.objects.filter(is_teacher=True)
    context = {'page': page, 'courses': courses, 'users':users, 'vcourses': vcourses}
    return render_to_response('index.html', context, RequestContext(request))


@login_required
def cabinet(request):
    context = {}
    return render_to_response('cabinet.html', context, RequestContext(request))



@login_required
def profile(request):
    courses = Course.objects.filter(is_active=True)
    vcourses = Vcourse.objects.filter(owner=request.user)
    profile = UserProfile.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
        return redirect('my_profile')
    else:
        form = ProfileForm(instance=profile)
    lessons = Subscriber2Lesson.objects.filter(user=request.user)
    context = {'form': form, 'profile':  profile, 'lessons': lessons, 'courses': courses, 'vcourses': vcourses}
    return render_to_response('profile.html', context, RequestContext(request))


def change_language(request):
    from django.conf import settings
    from django.utils import translation
    _next = request.REQUEST.get('next', None)
    if not _next:
        _next = request.META.get('HTTP_REFERER', None)

    if not _next:
        _next = '/'
    # если уже есть языковой префикс URL, надо убрать его
    for supported_language in settings.LANGUAGES:
        prefix = '/%s/' % supported_language[0]
        if _next.startswith(prefix):
            _next = _next[len(prefix):]
            break
    language = request.REQUEST.get(u'language', None)
    if _next == '/':
        response = HttpResponseRedirect('/')
    else:
        response = HttpResponseRedirect('/%s/%s' % (language, _next))

    if hasattr(request, 'session'):
        request.session['django_language'] = language
    else:
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)

    translation.activate(language)
    return response


