# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
import pandas as pd
import json
from critic.models import *
from django.views.generic.edit import FormView
from .models import Network, Show
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
# Create your views here.


def homeviewfunc(request):
    shows = ['westworld','game of thrones','insecure','westworld','house of cards','true detective','the deuce','master of none','bojack horseman', 'ballers','transparent','stranger things']
    show_list = Show.objects.filter(name__in=shows)
    movie_list = Show.objects.filter(category='movie')
    return render(request,'base.html',{'show_list':show_list,'movie_list':movie_list})

def aboutviewfunc(request):
    shows = ['westworld','game of thrones','insecure','westworld','house of cards','true detective','the deuce','master of none','bojack horseman', 'ballers','transparent','stranger things']
    show_list = Show.objects.filter(name__in=shows)
    movie_list = Show.objects.filter(category='movie')
    return render(request,'about.html',{'show_list':show_list,'movie_list':movie_list})

def contactviewfunc(request):
    shows = ['westworld','game of thrones','insecure','westworld','house of cards','true detective','the deuce','master of none','bojack horseman', 'ballers','transparent','stranger things']
    show_list = Show.objects.filter(name__in=shows)
    movie_list = Show.objects.filter(category='movie')
    return render(request,'contact.html',{'show_list':show_list,'movie_list':movie_list})

def showdetailfunc(request,slug):
    shows = ['westworld','game of thrones','insecure','westworld','house of cards','true detective','the deuce','master of none','bojack horseman', 'ballers','transparent','stranger things']
    show_list = Show.objects.filter(name__in=shows)
    movie_list = Show.objects.filter(category='movie')
    review_list = Reviews.objects.all()
    critics = Critic.objects.all()
    template_name = 'Twttr/show_detail.html'
    show_exists = Show.objects.filter(slug__iexact=slug)
    movie_exists = Movie.objects.filter(slug__iexact=slug)
    
    print show_exists
    print movie_exists
    if movie_exists and show_exists:
        print "route 1"
        
        show = Show.objects.get(slug=slug)
        
        critic_score=0
        pos_revs=0
        total_revs=0
        for item in Reviews.objects.filter(movie=Movie.objects.get(slug__iexact=slug)):
            total_revs+=1
            if item.thumbsup == 'Positive':
                pos_revs+=1
        critic_score = float(pos_revs)/float(total_revs)
        

        tweet_sentiment_addr = "/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/static/content/"+str(show.name).replace(' ','_')+"/sentiment_graphs/twitterdata.csv"
        df = pd.read_csv(tweet_sentiment_addr)
        print df
        twtr_score = float("{0:.2f}".format(df.NetPositive.iloc[-1]))
        try:
            chg = float("{0:.2f}".format(df.NetPositive.iloc[-1]-df.NetPositive.iloc[-2]))
        except:
            chg = 0
        if chg>0:
            chg = "+"+str(chg)
        try: 
            print 'it exists'
            mymov = Movie.objects.get(slug__iexact=slug)
            reviews = Reviews.objects.filter(movie=mymov)
            template_name='Twttr/show_detail.html'
        except:
            reviews = 0
            template_name='Twttr/show_detail.html'
        context = {'show_list':show_list,'show':show,'tweet_sentiment_addr':tweet_sentiment_addr,'twtr_score':twtr_score,'chg':chg,'movie_list':movie_list,'reviews':reviews,'critic_score':critic_score*100,'pos_revs':pos_revs,'total_revs':total_revs}
        
        return render(request,template_name,context)
    
    if movie_exists and not show_exists:
        print "route 2"
        
        mymov = Movie.objects.get(slug__iexact=slug)
        reviews = Reviews.objects.filter(movie=mymov)
        context = {'show_list':show_list,'movie_list':movie_list,'reviews':reviews}
        return render(request,template_name,context)
    
    if show_exists and not movie_exists:
        print "route 3"
        show=Show.objects.get(slug=slug)
        
        tweet_sentiment_addr = "/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/static/content/"+str(show.name).replace(' ','_')+"/sentiment_graphs/twitterdata.csv"
        df = pd.read_csv(tweet_sentiment_addr)
        print df
        twtr_score = float("{0:.2f}".format(df.NetPositive.iloc[-1]))
        try:
            chg = float("{0:.2f}".format(df.NetPositive.iloc[-1]-df.NetPositive.iloc[-2]))
        except:
            chg = 0
        if chg>0:
            chg = "+"+str(chg)
            
        context = {'show_list':show_list,'show':show,'tweet_sentiment_addr':tweet_sentiment_addr,'twtr_score':twtr_score,'chg':chg,'movie_list':movie_list}
        
        return render(request,template_name,context)
        
def search_func(request):
    
    search = request.GET.get('searchquery')
    
    search_text = search
    print "search text is %s" % (search_text)    
    show_obj = get_object_or_404(Show,name=search_text)
    show_slug = show_obj.slug
    
    
    
    return redirect('showdetailfunc', slug=show_slug)
    
    
        
        

class AutoCompleteView(FormView):
    def get(self,request,*args,**kwargs):
        data = request.GET
        showname = data.get("term")
        if showname:
            users = Show.objects.filter(name__icontains= showname)
        else:
            users = Show.objects.all()
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.name
            user_json['label'] = user.name
            user_json['value'] = user.name
            results.append(user_json)
            data = json.dumps(results)
            mimetype = 'application/json'
        return HttpResponse(data, mimetype)        
        
        
    

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

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response    
    
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