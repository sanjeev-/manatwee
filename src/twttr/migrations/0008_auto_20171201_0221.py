# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-01 02:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twttr', '0007_auto_20171130_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='twittercontent',
            name='sentiment',
            field=models.CharField(default='Neutral', max_length=120),
        ),
        migrations.AlterField(
            model_name='twittercontent',
            name='timeoftweet',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 1, 2, 21, 2, 698430)),
        ),
    ]
