# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 06:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_auto_20170527_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]