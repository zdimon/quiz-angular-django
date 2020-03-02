from ajax_upload.widgets import AjaxClearableFileInput
from django import forms
from videolearn.models import *
from ajax_upload.widgets import AjaxClearableFileInput
from ckeditor.widgets import CKEditorWidget
from image_cropping import ImageCropWidget




        


class VcourseForm(forms.ModelForm):
    class Meta:
        model = Vcourse
        fields = ( 'name', 'desc', 'requirements' ,'image', 'cropping', 'owner', 'price', 'type' )
        widgets = {
            'desc': CKEditorWidget(config_name='small'),
            'requirements': CKEditorWidget(config_name='small'),
            'image': ImageCropWidget,
            'owner': forms.HiddenInput(),
        }



class VlessonForm(forms.ModelForm):
    class Meta:
        model = Vlesson
        fields = ( 'number', 'name' , 'desc', 'owner', 'course', 'video', 'price' )
        widgets = {
            'owner': forms.HiddenInput(),
            'course': forms.HiddenInput(),
            'desc': CKEditorWidget(config_name='small'),
        }



class VarticleForm(forms.ModelForm):
    class Meta:
        model = Varticles
        fields = ( 'name', 'desc', 'adesc', 'lesson', 'sound', 'owner', 'is_free' )
        widgets = {
            'owner': forms.HiddenInput(),
            'lesson': forms.HiddenInput(),
        }       

