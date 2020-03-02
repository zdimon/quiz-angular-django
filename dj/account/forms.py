from django.forms import ModelForm, HiddenInput, TextInput, DateInput, SelectDateWidget
from .models import Profile
from image_cropping import ImageCropWidget
from django.contrib.admin.widgets import AdminDateWidget

# Create the form class.
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'avatar': ImageCropWidget,
            'user': HiddenInput(),
            'birthday': SelectDateWidget(years=range(1920, 2015))
            #'first_name': TextInput(attrs={'require': True})
        }
        exclude = ('wins', 'account')