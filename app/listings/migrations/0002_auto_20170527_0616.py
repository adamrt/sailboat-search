# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("listings", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="price",
            field=models.PositiveIntegerField(blank=True, null=True),
        )
    ]
