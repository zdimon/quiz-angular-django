# vim:fileencoding=utf-8
from optparse import make_option
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy as _
import time
from main.tasks import charge_for_chat
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)
logger.setLevel('DEBUG')

  

class Command(BaseCommand):
    

    def handle(self, *args, **options):
        print 'Start'
        charge_for_chat()
        print 'Fineshed '
        

