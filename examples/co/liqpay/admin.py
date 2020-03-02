from django.contrib import admin
from models import Liqpay
# Register your models here.

class LiqpayAdmin(admin.ModelAdmin):
    list_filter = ('is_success', )
    list_display = ( 'user', 'created', 'is_success' )

admin.site.register(Liqpay, LiqpayAdmin)
