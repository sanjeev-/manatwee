# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-06 18:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twttr', '0020_auto_20171206_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twittercontent',
            name='timeoftweet',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 6, 18, 49, 14, 221974)),
        ),
    ]
