# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Network, Show, TwitterUser

# Register your models here.

admin.site.register(Network)
admin.site.register(Show)
admin.site.register(TwitterUser)
