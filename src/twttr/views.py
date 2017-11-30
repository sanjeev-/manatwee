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