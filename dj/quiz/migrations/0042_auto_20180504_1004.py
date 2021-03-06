# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-04 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0041_auto_20180327_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='mode',
            field=models.CharField(default='fullmatch', help_text='Type of matching', max_length=10),
        ),
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.IntegerField(default='1', help_text='Order'),
        ),
        migrations.AlterField(
            model_name='question',
            name='tp',
            field=models.CharField(default='questionend', help_text='Mode of quize', max_length=12),
        ),
        migrations.AlterField(
            model_name='room',
            name='type',
            field=models.CharField(choices=[('questionend', 'Till questions are fineshed.'), ('infinite', 'Infinite quize (looping over questions).'), ('custom', 'Custom. Defining question by author.')], default='questionend', max_length=10, verbose_name='Quiz type'),
        ),
    ]
