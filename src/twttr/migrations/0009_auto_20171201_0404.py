# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-01 04:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twttr', '0008_auto_20171201_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twittercontent',
            name='timeoftweet',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 1, 4, 4, 36, 655857)),
        ),
    ]
