# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from datetime import datetime
from django.db.models.signals import pre_save, post_save
from twttr.utils import unique_slug_generator


right_now = datetime.now()
# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name    

class Critic(models.Model):
    name = models.CharField(max_length=120)
    organization = models.ForeignKey('Organization',on_delete=models.CASCADE,default=1)
    homeurl = models.CharField(max_length=560)
    critic_type = models.CharField(max_length=120,default='normal')
    

    
    def __unicode__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=120)
    
    def __unicode__(self):
        return self.name    

    
class Movie(models.Model):
    name = models.CharField(max_length=280)
    director = models.ForeignKey('Director',on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True,max_length=255)
    twitter_score = models.FloatField(null=True,blank=True,default=0.0)
    critics_score = models.FloatField(null=True,blank=True,default=0.0)
    

    def __unicode__(self):
        return self.name

    @property
    def title(self):
        return self.name
    
class Reviews(models.Model):
    movie=models.ForeignKey('Movie',on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    review_url = models.CharField(max_length=560)
    review_polarity = models.CharField(max_length=120)
    review_subjectivity = models.CharField(max_length=120)
    critic = models.ForeignKey('Critic',on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization',on_delete=models.CASCADE,default=1)
    text = models.TextField()
    blurb = models.TextField(null=True, blank=True)
    thumbsup = models.CharField(max_length=150,default='Positive')
    
    def __unicode__(self):
        return self.text

def show_pre_save_receiver(sender, instance, *args, **kwargs):
    print 'saving...'
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

def show_post_save_receiver(sender,instance,*args,**kwargs):
    print('saved')

    
pre_save.connect(show_pre_save_receiver,sender=Movie)

post_save.connect(show_post_save_receiver,sender=Movie)