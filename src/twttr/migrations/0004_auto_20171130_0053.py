# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-30 00:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twttr', '0003_auto_20171129_2326'),
    ]

    operations = [
        migrations.AddField(
            model_name='network',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='twitteruser',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
