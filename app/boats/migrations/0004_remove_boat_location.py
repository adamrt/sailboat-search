# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 16:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boats', '0003_boat_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boat',
            name='location',
        ),
    ]