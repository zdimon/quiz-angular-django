from django.contrib import admin

# Register your models here.

from ckeditor.fields import CKEditorWidget

from django.contrib.flatpages.admin import FlatPageAdmin, FlatpageForm
from django.contrib.flatpages.models import FlatPage
from main.models import UserProfile

class MyFlatpageForm(FlatpageForm):
    widgets = {
            'content' : CKEditorWidget(),
        }

class MyFlatPageAdmin(FlatPageAdmin):
    form = MyFlatpageForm
    class Media:
        js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
              '/static/grappelli/tinymce_setup/tinymce_setup.js']

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, MyFlatPageAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("thumb", "first_name", "last_name", "email", "is_teacher")
admin.site.register(UserProfile, UserProfileAdmin)
