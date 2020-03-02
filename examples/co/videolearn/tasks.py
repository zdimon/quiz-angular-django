# vim:fileencoding=utf-8
import datetime
from celery import task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives
import os



@task(name='convert')
def convert():
    from videolearn.models import Vlesson
    from subprocess import call
    import subprocess
    from ffvideo import VideoStream
    from django.core.files import File
    from co.settings import BASE_DIR
    for v in Vlesson.objects.filter(is_converted=False):
        ex =  'avconv -i %s -ar 22050 -crf 28 %s.flv' % (v.video.path,v.video.path)
        print ex 
        return_code = call(ex,shell=True)
        print return_code
        if(return_code==1):
            p = subprocess.Popen(ex, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            v.is_error = True
            v.error_desc = str(p.stdout.read())
            v.save()
        else:
            v.is_converted = True
            
            with open(v.video.path):
                vs = VideoStream(v.video.path+'.flv',frame_size=(800, None))
                token = 'screen_%s' % v.id
                thumb = BASE_DIR+'/media/vcourse_images/'+token+'.jpg'
                print 'Time:::: %s' % vs.duration 
                #duration = int(vs.duration)
                duration = 2
                frame = vs.get_frame_at_sec(duration)
                frame.image().save(thumb)
                f = File(open(thumb))
                v.image.save(thumb,f)
            dur = int(vs.duration/60)
            durs = ' %s sec (%s min)' % (vs.duration,str(dur))
            v.duration = durs
            v.save()

        ''''  
        try:
            res = os.system(ex).read()
        except Exception, e:
            print 'ddddddddddddddddddd %s' % e
            v.is_error = True
            v.error_desc = str(e)
            v.save()
        print res
        '''
#avconf -i test.mp4 -ar 22050 -ab 32 -f flv -s 1.flv

#avconf -i test.mp4 -c:v libx264 -ar 22050 -crf 28 destinationfile.flv

#avconv -i /home/zdimon/hd/www/co_ve/co/media/vcourse_video/40c8cb26c02449828b69c69605a4dd26.mp4 -c:v libx264 -ar 22050 -crf 28 /home/zdimon/hd/www/#co_ve/co/media/vcourse_video/40c8cb26c02449828b69c69605a4dd26.mp4.flv
