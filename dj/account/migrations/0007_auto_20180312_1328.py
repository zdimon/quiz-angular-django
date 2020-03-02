# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-12 13:28
from __future__ import unicode_literals

from django.db import migrations
import django_countries.fields
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20180216_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cropping',
            field=image_cropping.fields.ImageRatioField('avatar', '100x100', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='Country'),
        ),
    ]
