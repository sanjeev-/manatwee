# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-30 23:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twttr', '0006_twittercontent_timeoftweet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twittercontent',
            name='timeoftweet',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 30, 23, 26, 5, 612914)),
        ),
    ]