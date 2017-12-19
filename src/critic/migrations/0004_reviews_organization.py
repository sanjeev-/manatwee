# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-06 18:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('critic', '0003_movie_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='critic.Organization'),
        ),
    ]
