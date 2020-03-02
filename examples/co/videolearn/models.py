from django.db import models
from django.utils.translation import ugettext as _
from ckeditor.fields import RichTextField
import pytils
from django.contrib.auth.models import User
from image_cropping import ImageCropField, ImageRatioField
from easy_thumbnails.files import get_thumbnailer
from django.utils.safestring import mark_safe
import os
from uuid import uuid4
from django.core.urlresolvers import reverse
from redactor.fields import RedactorField


class Vcourse(models.Model):
    TYPES = ( ('v', _('Video')), ('a', _('Audio')) )
    type = models.CharField(max_length = 2, choices = TYPES, default = 'v', verbose_name = _('Type'))
    name = models.CharField(max_length=250, blank=True, verbose_name=_(u'Name'))
    desc = models.TextField(blank=True, verbose_name=_(u'Description'))
    requirements = models.TextField(blank=True, verbose_name=_(u'Requirements'))
    owner = models.ForeignKey(User, verbose_name=_(u'Owner'))
    image = models.ImageField(blank=True, verbose_name=_(u'Image'), upload_to='vcourse_images', null = True)
    cropping = ImageRatioField('image', '200x200', size_warning=True)
    is_active = models.BooleanField(verbose_name=_('Is published?'), default=False)
    on_delete = models.BooleanField(verbose_name=_('Deleted?'), default=False)
    name_slug = models.CharField(verbose_name='Name slug',max_length=250, blank=True)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
       return reverse("vcourse-detail", kwargs={"slug": self.name_slug})
    @property
    def thumb(self):
        try:
            thumbnail_url = get_thumbnailer(self.image).get_thumbnail({
                'size': (100, 100),
                'box': self.cropping,
                'crop': True,
                'detail': True,
            }).url
            return mark_safe(u'<img src="%s" />' % thumbnail_url)
        except:
            return 'no image'
    def save(self, **kwargs):
        if not self.id:
            self.name_slug = pytils.translit.slugify(self.name)
        return super(Vcourse, self).save(**kwargs)

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper

class Vlesson(models.Model):
    name = models.CharField(max_length=250, blank=True, verbose_name=_(u'Name'))
    desc = models.TextField(blank=True, verbose_name=_(u'Description'))
    is_active = models.BooleanField(verbose_name=_('Is main?'), default=False)
    owner = models.ForeignKey(User, verbose_name=_(u'Owner'))
    course = models.ForeignKey(Vcourse, verbose_name=_(u'Course'), blank=True, null = True)
    video = models.FileField(blank=True, verbose_name=_(u'Video'), upload_to=path_and_rename('vcourse_video'), null = True)
    is_converted = models.BooleanField(verbose_name=_('Is converted?'), default=False)
    is_error = models.BooleanField(verbose_name=_('Is converted?'), default=False)
    error_desc = models.TextField(blank=True, verbose_name=_(u'Error description'))
    is_free = models.BooleanField(verbose_name=_('Is free?'), default=False)
    name_slug = models.CharField(verbose_name='Name slug',max_length=250, blank=True)
    duration = models.CharField(verbose_name='Duration',max_length=250, blank=True)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    is_public = models.BooleanField(verbose_name=_('Is public?'), default=True)
    image = models.ImageField(blank=True, verbose_name=_(u'Image'), upload_to='vcourse_images', null = True)
    cropping = ImageRatioField('image', '200x155', size_warning=True)
    number = models.PositiveIntegerField(
        verbose_name=_(u'Number'),
        default=0)
    def get_absolute_url(self):
       return reverse("start-lecture", kwargs={"id": self.id})
    @property
    def file_name(self):
        return str(self.video).split('/')[1]     
    @property
    def screenshot(self):
        try:
            thumbnail_url = get_thumbnailer(self.image).get_thumbnail({
                'size': (200, 155),
                'box': self.cropping,
                'crop': True,
                'detail': True,
            }).url
            return mark_safe(u'<img src="%s" />' % thumbnail_url)
        except:
            return 'no image'
        return 'no'

        
 
    @property
    def price_str(self):
        if self.is_free or self.price == 0:
            return u'free'
        else:
            return self.price    

    def __unicode__(self):
        return self.name
    def save(self, **kwargs):
        if not self.id:
            self.name_slug = pytils.translit.slugify(self.name)
            if self.video.path.split('.')[-1] == 'flv':
                self.is_converted = True
        return super(Vlesson, self).save(**kwargs)


def gidrate_lessons(lessons,user):
    from liqpay.models import Liqpay
    #import pdb; pdb.set_trace()
    for l in lessons:
        if l.price==0:
            l.is_byed = True
        else:
            try:
                b = Liqpay.objects.get(user=user,lesson=l,is_success=True)
                l.is_byed = True
            except:
                l.is_byed = False   
    return lessons


class Varticles(models.Model):
    name = models.CharField(max_length=250, blank=True, verbose_name=_(u'Name'))
    desc = RedactorField(blank=True, verbose_name=_(u'Description'))
    adesc = RedactorField(blank=True, verbose_name=_(u'Description additional'))
    lesson = models.ForeignKey(Vlesson, verbose_name=_(u'Course'), blank=True, null = True)
    name_slug = models.CharField(verbose_name='Name slug',max_length=250, blank=True)
    pub = models.BooleanField(verbose_name=_('Is published?'), default=True)
    sound = models.FileField(blank=True, verbose_name=_(u'Sound'), upload_to=path_and_rename('vcourse_sound'), null = True)
    owner = models.ForeignKey(User, verbose_name=_(u'Owner'))
    is_free = models.BooleanField(verbose_name=_('Is free?'), default=False)
    def get_absolute_url(self):
       return reverse("article-detail", kwargs={"id": self.id})
    def __unicode__(self):
        return self.name
    def save(self, **kwargs):
        if not self.id:
            self.name_slug = pytils.translit.slugify(self.name)
        return super(Varticles, self).save(**kwargs)

class Vsounds(models.Model):
    sound = models.FileField(blank=True, verbose_name=_(u'Sound'), upload_to=path_and_rename('vcourse_sound'), null = True)
    article = models.ForeignKey(Varticles)
    pub = models.BooleanField(verbose_name=_('Is published?'), default=True)

class Vimages(models.Model):
    image = models.ImageField(blank=True, verbose_name=_(u'Image'), upload_to='course_images')
    cropping = ImageRatioField('image', '100x100', size_warning=True)
    article = models.ForeignKey(Varticles)
    def __unicode__(self):
        thumbnail_url = get_thumbnailer(self.image).get_thumbnail({
            'size': (100, 100),
            'box': self.cropping,
            'crop': True,
            'detail': True,
        }).url
        return mark_safe(u'<img src="%s" />' % thumbnail_url)
    @property
    def thumb(self):
        thumbnail_url = get_thumbnailer(self.image).get_thumbnail({
            'size': (250, 250),
            'box': self.cropping,
            'crop': True,
            'detail': True,
        }).url
        return mark_safe(u'<img src="%s" />' % thumbnail_url)



class Access(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=True, blank=True, null=True)
    user = models.ForeignKey(User)
    lesson = models.ForeignKey(Vlesson, verbose_name=_(u'Lesson'), blank=True, null = True)
    alias = models.CharField(verbose_name='Alias',max_length=250, blank=True)
    def save(self, **kwargs):
        from co.settings import BASE_DIR
        from subprocess import call
        if not self.id:
            fname = uuid4().hex
            self.alias = fname
            lnk = 'ln -P %s %s' % (self.lesson.video.path,BASE_DIR+'/media/access/'+fname+'.flv')
            print lnk
            call(lnk,shell=True)
        return super(Access, self).save(**kwargs)
