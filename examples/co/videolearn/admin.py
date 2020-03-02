from django.contrib import admin
from videolearn.models import *
# Register your models here.

class VcourseAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "on_delete")


admin.site.register(Vcourse, VcourseAdmin)

