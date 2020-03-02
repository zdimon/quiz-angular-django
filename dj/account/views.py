# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
#from registration.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail
from account.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect
from registration.backends.hmac.views import RegistrationView, ActivationView
from registration import signals
from django.contrib.auth import authenticate, login
from registration.signals import user_activated
from registration.models import RegistrationProfile
from .forms import ProfileForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.shortcuts import resolve_url
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.response import Response
import json
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from dj.settings import BASE_DIR
# Create your views here.

@csrf_exempt
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def save_pic(request):
    
    input_data = request.POST['data']
    user_id = request.POST['user_id']
    account = Profile.objects.get(pk=user_id)
    img_name = '%s.png' % user_id
    

    input_data = input_data.replace('data:image/png;base64,','')

    #print input_data
    path = '%s/media/%s' % (BASE_DIR, img_name)
    f = open(path,'wb')
    f.write(input_data.decode('base64'))
    f.close()
    account.avatar.save( img_name,File(open(path)))     
    return Response({
        'status': 0
    })

def check_session(request):
    try:
        token =  request.session['try_room']
        del request.session['try_room']
        return redirect('quiz:room_detail', token=token)
    except:
        return redirect('mainpage') 


class RegForm(RegistrationFormUniqueEmail):
    def __init__(self, *args, **kwargs):
        super(RegistrationFormUniqueEmail,self).__init__(*args, **kwargs)
        del self.fields['username']

class MyLoginView(auth_views.LoginView):   
    def get_success_url(self):
        """Ensure the user-originating redirection URL is safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        '''
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        '''
        #try:
        #try:
        if self.request.method == "POST":
            try:
                token =  self.request.session['try_room']
                del self.request.session['try_room']
                return resolve_url('quiz:room_detail', token)
            except:
                pass
            #return '/quiz/room/%s' % self.request.session['try_room']
        #if not url_is_safe:
        return resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to

class MyRegistrationView(RegistrationView):
    form_class = RegForm
    def register(self, form):
        p = User()
        p.username = form.cleaned_data['email']
        p.email = form.cleaned_data['email']
        p.set_password(form.cleaned_data['password1'])
        p.is_active = False
        p.save()
        RegistrationProfile.objects.create_profile(p)

        signals.user_registered.send(sender=self.__class__,
                                     user=p,
                                     request=self.request)
        self.send_activation_email(p)
        return p

    def get_success_url(self, user):
        return ('registration_done', (), {})

class MyActivationView(ActivationView):   
    success_url = 'activation_done'
    def activate(self, *args, **kwargs):
        #import pdb; pdb.set_trace()
        username = self.validate_key(kwargs.get('activation_key'))
        if username is not None:
            user = self.get_user(username)
            if user is not None:
                user.is_active = True
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(self.request, user)
                #return redirect('profile_edit')
                return user
        return False

class ProfileEditView(UpdateView):
    model = Profile
    form_class = ProfileForm
    
    def get_object(self, queryset=None):
        obj = Profile.objects.get(user=self.request.user)
        return obj
    def get_success_url(self):
        return reverse('profile_edit')
    def form_valid(self, form):
        messages.success(self.request, _('You profile has been saved successfully.'))
        return super(ProfileEditView,self).form_valid(form)        
    

def registration_done(request):
    return render(request, 'account/registration_done.html')

def activation_done(request):
    #print request.session['try_room']
    #import pdb; pdb.set_trace()
    try:
        token =  request.session['try_room']
        del request.session['try_room']
    except:
        token = None
    return render(request, 'account/activate.html', { 'token':token })

def show(request):
    return render(request, 'account/show.html')
