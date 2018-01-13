# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from twttr.models import *
from critic.models import *
from django.contrib.auth.models import User


from django.db import models

# Create your models here.

class RNNCriticData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    review = models.ForeignKey('critic.Reviews',on_delete=models.CASCADE)
    markedsentiment = models.IntegerField()

class RNNTwitterData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    review = models.ForeignKey('twttr.TwitterContent',on_delete=models.CASCADE)
    markedsentiment = models.IntegerField()
    