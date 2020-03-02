# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from image_cropping import ImageRatioField
from image_cropping.utils import get_backend
# Create your models here.

class Profile(models.Model):
    '''
        Профиль пользователя.
    '''
    gender = (
        ('m', _('Male')),
        ('f', _('Female'))
    )
    user = models.OneToOneField(User, primary_key=True, verbose_name=_(u"User"))
    wins = models.IntegerField(verbose_name=_(u"Wins"), default=0)
    account = models.IntegerField(verbose_name=_(u"Account"), default=0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name=_(u'Image'))
    phone = models.CharField(max_length=50, blank=True, verbose_name=_(u'Phone number'))
    rating = models.IntegerField(default=0, null=True, blank=True, verbose_name=_(u'Rating'))
    birthday = models.DateField(null=True, blank=True, verbose_name=_(u'Birthday'))
    gender = models.CharField(verbose_name=_(u'Gender'), max_length=10, choices=gender, default='m')
    country = CountryField(verbose_name=_(u'Country'), null=True, blank=True)
    is_online = models.BooleanField(default=False, verbose_name=_(u'Is online?'))
    ip_address = models.CharField(max_length=50, blank=True, verbose_name=_(u'IP address'))
    cropping = ImageRatioField('avatar', '100x100')

    def get_small_avatar_url(self):
        try:
            thumbnail_url = get_backend().get_thumbnail_url(
                self.avatar,
                {
                    'size': (50, 50),
                    'box': self.cropping,
                    'crop': True,
                    'detail': True,
                }
            )
            return thumbnail_url
        except:
            return '/static/image/noavatar.png'

    def get_username(self):
        return self.user.username

    def get_avatar_url(self):
        try:
            return self.avatar.url
        except:
            return '/static/image/noavatar.png'

    def get_rating(self):
        return self.wins

'''
    Creating profile when got a signal.
'''

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)



class Transaction(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'User'))
    ammount = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name=_(u'Ammount'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_(u'Created at'))


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

        