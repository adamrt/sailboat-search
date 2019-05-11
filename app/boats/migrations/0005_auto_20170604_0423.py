# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-04 04:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("boats", "0004_remove_boat_location")]

    operations = [
        migrations.AddField(
            model_name="boat", name="favorite", field=models.BooleanField(default=False)
        ),
        migrations.AddField(
            model_name="boat", name="sd_url", field=models.URLField(blank=True)
        ),
    ]
