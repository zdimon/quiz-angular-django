# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-06 14:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0015_remove_roomquestion_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomquestion',
            old_name='quiestion',
            new_name='question',
        ),
    ]
