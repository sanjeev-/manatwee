# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
from django.db.models import Q
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
import pandas as pd
import json
from critic.models import *
from django.views.generic.edit import FormView
from .models import *
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
# Create your views here.
from .forms import ContactForm, RNNCriticForm
from RNN.models import *


def homeviewfunc(request):
    shows = ['westworld','game of thrones','insecure','westworld','house of cards','true detective','the deuce','master of none','bojack horseman', 'ballers','transparent','stranger things']
    show_list = Show.objects.filter(name__in=shows)
    movie_list = Show.objects.filter(network=Network.objects.get(name='MOVIES'))
    
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
    form = ContactForm()
    if request.method == "GET":
        form = ContactForm()
        return render(request,'contact.html',{'show_list':show_list,'movie_list':movie_list,'form':form})
    
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
            
        return render(request,'contact.html',{'show_list':show_list,'movie_list':movie_list,'form':form,'text':text})
        
    
    return render(request,'contact.html',{'show_list':show_list,'movie_list':movie_list,'form':form})

def showdetailfunc(request,slug):
    shows = ['westworld','game of thrones','insecure','westworld','house of cards','true detective','the deuce','master of none','bojack horseman', 'ballers','transparent','stranger things']
    show_list = Show.objects.filter(name__in=shows)
    movie_list = Show.objects.filter(network=Network.objects.get(name='MOVIES'))
    review_list = Reviews.objects.all()
    critics = Critic.objects.all()
    template_name = 'Twttr/show_detail.html'
    show_exists = Show.objects.filter(slug__iexact=slug)
    movie_exists = Movie.objects.filter(slug__iexact=slug)
    user = request.user
    form=RNNCriticForm()
    
    if request.method == "POST":
        print 'received post'
        usr= request.user
        critic_name = request.POST.get('critic_name',default=None)
        movie_name = request.POST.get('movie_name',default=None)
        org_name = request.POST.get('org_name',default=None)
        criticdata=Critic.objects.get(name=critic_name)
        moviedata = Movie.objects.get(name=movie_name)
        orgdata = Organization.objects.get(name=org_name)
        review_model = Reviews.objects.get(movie=moviedata,critic=criticdata,organization=orgdata)
        print review_model
        ms = int(request.POST.get('markedsentiment',default=None))
        datum = RNNCriticData(review=review_model,user=usr,markedsentiment=ms)
        datum.full_clean()
        datum.save()
        print 'saved datapt to database'

    
    if movie_exists and show_exists:
        print "route 1"
        
        show = Show.objects.get(slug=slug)
        
        last = len(TwitterContent.objects.filter(show=show))
        tweetlist = TwitterContent.objects.filter(show=show)[last-26:last-1]
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
        twtr_score = float("{0:.2f}".format(df.NetPositive.iloc[-1]))
        try:
            chg = float("{0:.2f}".format(df.NetPositive.iloc[-1]-df.NetPositive.iloc[-2]))
        except:
            chg = 0
        if chg>0:
            chg = "+"+str(chg)
        try: 
            mymov = Movie.objects.get(slug__iexact=slug)
            reviews = Reviews.objects.filter(movie=mymov)
            template_name='Twttr/show_detail.html'
        except:
            reviews = 0
            template_name='Twttr/show_detail.html'
        context = {'show_list':show_list,'show':show,'tweet_sentiment_addr':tweet_sentiment_addr,'twtr_score':twtr_score,'chg':chg,'movie_list':movie_list,'reviews':reviews,'critic_score':critic_score*100,'pos_revs':pos_revs,'total_revs':total_revs,'tweetlist':tweetlist,'form':form}
        
        return render(request,template_name,context)
    
    if movie_exists and not show_exists:
        print "route 2"
        
        mymov = Movie.objects.get(slug__iexact=slug)
        reviews = Reviews.objects.filter(movie=mymov)
        context = {'show_list':show_list,'movie_list':movie_list,'reviews':reviews,'form':form}
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
            
        context = {'show_list':show_list,'show':show,'tweet_sentiment_addr':tweet_sentiment_addr,'twtr_score':twtr_score,'chg':chg,'movie_list':movie_list,'form':form}
        
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