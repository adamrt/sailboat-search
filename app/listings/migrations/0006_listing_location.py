# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_auto_20170527_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='location',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]