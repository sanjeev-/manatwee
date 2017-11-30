# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator

# Create your models here.

class Network(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, null=True, blank=True)
    category = models.CharField(max_length=120, blank=False,default='television')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name

class Show(models.Model):
    name = models.CharField(max_length=120)
    network = models.ForeignKey('Network',on_delete=models.CASCADE)
    genre = models.CharField(max_length=120, null=True, blank=True)
    category = models.CharField(max_length=120, blank=False,default='television')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  
    slug = models.SlugField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
    @property
    def title(self):
        return self.name

    
class TwitterUser(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, null=True, blank=True)
    category = models.CharField(max_length=120, blank=False,default='normal')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)
    
    def __unicode__(self):
        return self.name

def show_pre_save_receiver(sender, instance, *args, **kwargs):
    print 'saving...'
    print(instance.timestamp)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

def show_post_save_receiver(sender,instance,*args,**kwargs):
    print('saved')
    print(instance.timestamp)
    
pre_save.connect(show_pre_save_receiver,sender=Show)

post_save.connect(show_post_save_receiver,sender=Show)