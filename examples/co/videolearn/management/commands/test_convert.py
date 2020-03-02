# -*- coding: utf-8 -*-

import logging
from optparse import make_option
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
import datetime

logger = logging.getLogger(__name__)


class Command(BaseCommand):
   

    def handle(self, *args, **options):
        print 'Start converting'
        from videolearn.tasks import convert
        convert()
        
