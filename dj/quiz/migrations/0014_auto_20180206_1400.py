# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-06 14:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_auto_20180206_1357'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RoomQuiestion',
            new_name='RoomQuestion',
        ),
    ]
