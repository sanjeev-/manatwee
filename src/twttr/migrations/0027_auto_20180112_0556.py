# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-12 05:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twttr', '0026_auto_20180112_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twittercontent',
            name='timeoftweet',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 12, 5, 56, 13, 919341)),
        ),
    ]
