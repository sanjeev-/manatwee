# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-05 19:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twttr', '0013_auto_20171205_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twittercontent',
            name='timeoftweet',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 5, 19, 57, 18, 851321)),
        ),
    ]