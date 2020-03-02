# vim:fileencoding=utf-8
from optparse import make_option
from django.core.management.base import BaseCommand
import time
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
logger.setLevel('DEBUG')
from django_faker import Faker
from course.models import Course
from django.contrib.auth.models import User
  

class Command(BaseCommand):
    

    def handle(self, *args, **options):
        populator = Faker.getPopulator()
        print 'Start'       
        owner = User.objects.get(pk=1)
        populator.addEntity(Course,5, {'owner':owner})
        insertedPks = populator.execute()
        print insertedPks
        print 'Fineshed '
        

