# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from critic.models import *
from django.views.generic.edit import FormView
from twttr.models import *

# Create your views here.

def register_view_func(request):
    shows = ['westworld','game of thrones','insecure','westworld','house of cards','true detective','the deuce','master of none','bojack horseman', 'ballers','transparent','stranger things']
    show_list = Show.objects.filter(name__in=shows)
    movie_list = Show.objects.filter(network=Network.objects.get(name='MOVIES'))
    
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
        
        args = {'form':form,'show_list':show_list,'movie_list':movie_list}
        return render(request,'Acct/registration.html',args)
            
    