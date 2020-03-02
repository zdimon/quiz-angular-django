import pickle
from course.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader, Context
from django.utils.translation import ugettext as _
from co.settings import VIDEO_SERVER
from main.models import UserProfile
    
# Get template with people online list
def owner_cam_template(lesson, user, type):
    t = loader.get_template('flash_cam.html')
    c = Context({'type': type, 'video_server': VIDEO_SERVER, 'token': 'lesson_%s' % lesson.id })
    return t.render(c)

def student_cam_template(lesson, user_id, type):
    t = loader.get_template('flash_cam_student.html')
    user = UserProfile.objects.get(pk=user_id)
    c = Context({'user': user, 'type': type, 'video_server': VIDEO_SERVER, 'token': 'lesson_%s_%s_student' % (lesson.id,user_id) })
    return t.render(c)   

def my_cam_template(user):
    t = loader.get_template('my_cam.html')
    c = Context({'video_server': VIDEO_SERVER, 'token': 'my_%s' % user.id })
    return t.render(c)
 

def add_user_if_not_exist(user,lesson):
    try:
        Users2Lesson.objects.get(user=user, lesson=lesson)
    except:
        Users2Lesson.objects.create(user=user, lesson=lesson)



def get_participants(lesson):
    users = []
    for u2l in Users2Lesson.objects.filter(lesson=lesson):
        users.append(u2l.user)
    return users

def get_participants_exclude_one(lesson,user):
    users = []
    for u2l in Users2Lesson.objects.filter(lesson=lesson).exclude(user=user):
        users.append(u2l.user)
    return users



def make_thumb(user):
    from ffvideo import VideoStream
    from co.settings import FLV_PATH
    from co.settings import BASE_DIR
    from shutil import copyfile
    from django.core.files import File
    token = 'my_%s' % user.id
    filename = FLV_PATH+'/'+token+'.flv'
    print filename
    #filenametmp = MEDIA_ROOT+'/video/'+token+'_tmp.flv'
    thumb = BASE_DIR+'/media/profile_images/'+token+'.jpg'
    #try:
    with open(filename):
        print ('converting:'+filename+' to '+thumb)
        #copyfile(filename,filenametmp)
        vs = VideoStream(filename,frame_size=(800, None))
        duration = int(vs.duration)
        duration = 1
        print('get frame number'+str(duration))
        #try:
        frame = vs.get_frame_at_sec(duration)
        frame.image().save(thumb)
        f = File(open(thumb))
        user.image.save(thumb,f)
    #            self.profile.save()
    #        except Exception, e:
    #            print e
    #except IOError:
    #    pass



def lesson_runing(lessons):
    t = loader.get_template('lesson_running_list.html')
    c = Context({'lessons': lessons })
    return t.render(c)


