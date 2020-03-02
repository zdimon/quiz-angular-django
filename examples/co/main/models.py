from django.db import models
from easy_thumbnails.files import get_thumbnailer
from image_cropping import ImageCropField, ImageRatioField
from django.contrib.auth.models import User, UserManager
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from decimal import Decimal

class UserProfile(User):
    image = models.ImageField(upload_to='profile_images', verbose_name='Image', blank=True)
    cropping = ImageRatioField('image', '100x100', size_warning=True)
    is_teacher = models.BooleanField(verbose_name=_('Is teacher?'), default=False)
    phone = models.CharField(max_length=250, blank=True, verbose_name=_(u'Phone'))
    desc = models.TextField(blank=True, verbose_name=_(u'About you'), help_text=_(u'Tell us about your please.'))
    is_cam_on = models.BooleanField(verbose_name=_('Is cam on?'), default=False)
    is_mic_on = models.BooleanField(verbose_name=_('Is mic on?'), default=False)
    account = models.DecimalField(max_digits=20,decimal_places=2,default=Decimal('0.00'))
    @property
    def thumb(self): 
        try:
            thumbnail_url = get_thumbnailer(self.image).get_thumbnail({
                'size': (50, 50),
                'box': self.cropping,
                'crop': True,
                'detail': True,
            }).url
            return mark_safe(u'<img id="user_participant_%s" title="%s" class="user_thumb" data-id="%s" src="%s" />' % (self.id, self.user_name, self.id, thumbnail_url))
        except:
            return mark_safe(u'<img id="user_participant_%s" title="%s" class="user_thumb" data-id="%s" src="/static/images/no-user.png" />' % (self.id, self.user_name,self.id))
    @property
    def user_name(self):
        if len(self.first_name)>0 or len(self.last_name)>0:
            return '%s %s' % (self.first_name, self.last_name)
        else:
            return self.username
    objects = UserManager()


from django.db.models.signals import post_save

def create_custom_user(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = UserProfile(**values)
        user.save()

post_save.connect(create_custom_user, User)


from django.dispatch import receiver
from registration.signals import user_activated
from django.contrib.auth import login


@receiver(user_activated)
def login_on_activation(sender, user, request, **kwargs):
    """Logs in the user after activation"""
    user.backend = 'main.auth.ProfileUserModelBackend'
    login(request, user)

