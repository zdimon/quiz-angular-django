from ajax_upload.widgets import AjaxClearableFileInput
from django import forms
from course.models import Images, Course, Lesson
from ajax_upload.widgets import AjaxClearableFileInput
from ckeditor.widgets import CKEditorWidget
from image_cropping import ImageCropWidget

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ( 'image', )
        widgets = {
            'image': AjaxClearableFileInput
        }





class AjaxImageForm(forms.Form):
    my_image_field = forms.ImageField(widget=AjaxClearableFileInput())


class ImportImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ( 'image', 'lesson', 'publish')
        


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ( 'name', 'desc', 'requirements' ,'image', 'cropping', 'owner' )
        widgets = {
            'desc': CKEditorWidget(config_name='small'),
            'requirements': CKEditorWidget(config_name='small'),
            'image': ImageCropWidget,
            'owner': forms.HiddenInput(),
        }



class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ( 'name' ,'image', 'desc', 'cropping', 'owner', 'course' )
        widgets = {
            'image': ImageCropWidget,
            'owner': forms.HiddenInput(),
            'course': forms.HiddenInput(),
            'desc': CKEditorWidget(config_name='small'),
        }

