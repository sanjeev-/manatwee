# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-04 20:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twttr', '0010_auto_20171201_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twittercontent',
            name='timeoftweet',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 4, 20, 6, 40, 314890)),
        ),
    ]
