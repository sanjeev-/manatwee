# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .models import Network, Show
# Create your views here.


def homeviewfunc(request):
    show_list = Show.objects.all()
    return render(request,'base.html',{'show_list':show_list})

def aboutviewfunc(request):
    show_list = Show.objects.all()
    return render(request,'about.html',{'show_list':show_list})

def contactviewfunc(request):
    show_list = Show.objects.all()
    return render(request,'contact.html',{'show_list':show_list})

def showdetailfunc(request,slug):
    show_list = Show.objects.all()
    template_name = 'Twttr/show_detail.html'
    show = Show.objects.filter(
                Q(slug__iexact=slug) |
                Q(slug__icontains=slug)
            )
    show = show[0]
    tweet_sentiment_addr = "/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/static/content/"+str(show.name).replace(' ','_')+"/sentiment_graphs/twitterdata.csv"
    context = {'show_list':show_list,'show':show,'tweet_sentiment_addr':tweet_sentiment_addr}
    return render(request,template_name,context)
    

class NetworkListView(ListView):
    queryset = Network.objects.all()
    template_name='Twttr/network_list.html'

class ShowListView(ListView):
    template_name = 'Twttr/show_list.html'
    
    def get_queryset(self):
        slug = self.kwargs.get("slug")
        if slug:
            queryset = Show.objects.filter(
                Q(name__iexact=slug) |
                Q(name__icontains=slug)
            )
        else:
            queryset = Show.objects.all()
        return queryset

    
class ShowDetailView(DetailView):
    template_name='Twttr/show_detail.html'
    queryset = Show.objects.all()
    def get_context_data(self,*args,**kwargs):
        print(self.kwargs)
        context = super(ShowDetailView,self).get_context_data(*args,**kwargs)
        print(context)
        return context
    
class HomeListView(ListView):
    queryset = Show.objects.all()
    template_name='base.html'
    
class AboutListView(ListView):
    queryset = Show.objects.all()
    template_name='about.html'
    
class ContactListView(ListView):
    queryset = Show.objects.all()
    template_name='contact.html'