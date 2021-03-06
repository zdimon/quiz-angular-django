# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-29 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField(max_length=100, verbose_name='\u0422\u0435\u043c\u0430')),
                ('email', models.TextField(blank=True, null=True, verbose_name='E-mail')),
                ('message', models.TextField(verbose_name='\u0421\u043e\u043e\u0431\u0449\u043d\u0435\u0438\u0435')),
                ('resolved', models.BooleanField(default=False, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('content', models.TextField(verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435')),
                ('alias', models.CharField(max_length=150, verbose_name='\u0410\u043b\u0438\u0430\u0441')),
                ('meta_title', models.CharField(max_length=150, verbose_name='\u041c\u0435\u0442\u0430-\u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('meta_keywords', models.CharField(max_length=250, verbose_name='\u041c\u0435\u0442\u0430-\u0441\u043b\u043e\u0432\u043e\u0441\u043e\u0447\u0438\u0442\u0430\u043d\u0438\u044f')),
                ('meta_description', models.CharField(max_length=250, verbose_name='\u041c\u0435\u0442\u0430-\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
            ],
        ),
    ]
