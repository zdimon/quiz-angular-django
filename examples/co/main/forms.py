# -*- coding: utf-8 -*-
from django.forms import ModelForm
from main.models import UserProfile
from image_cropping import ImageCropWidget

class ProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = [ 'first_name',
                   'last_name',
                   'desc',
                   'image',
                   'email',
                   'phone',
                   'cropping',
                 ]
        widgets = {
            'image': ImageCropWidget,
        }

    #def __init__(self, user, *args, **kwargs):
    #    kwargs['instance'] = user
    #    super(ProfileForm, self).__init__(*args, **kwargs)       
