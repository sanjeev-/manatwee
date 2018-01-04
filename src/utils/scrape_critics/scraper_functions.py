import os, errno, sys
from bs4 import BeautifulSoup
from requests import get
from textblob import TextBlob
import pandas as pd
from pyteaser import Summarize
from django.utils.encoding import smart_str, smart_unicode


proj_path = "/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manatwee.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from twttr.models import *
from critic.models import *


def reviewsDictToDatabase(mydict,name_of_publication):
    
    if Organization.objects.filter(name=name_of_publication).exists():
        print 'Organization %s already exists!' % (name_of_publication)
    else:
        newOrg = Organization(name=name_of_publication)
        newOrg.save()
        print 'added %s to the Organization Database' % (name_of_publication)
    
    myOrg = Organization.objects.get(name=name_of_publication)
    defaultDir = Director.objects.all()[0]
    
    for movie_review in mydict:
        r_name = mydict[movie_review]['name']
        r_critic = mydict[movie_review]['critic']
        r_link = mydict[movie_review]['link']
        r_text = mydict[movie_review]['text']
        r_blurb = mydict[movie_review]['blurb']
        r_sentiment = mydict[movie_review]['sentiment']
        r_thumbsup = mydict[movie_review]['thumbsup']
        r_subjectivity = mydict[movie_review]['review_subjectivity']
        r_polarity = mydict[movie_review]['review_polarity']
        if Movie.objects.filter(name=r_name).exists():
            print '%s movie already exists in the Database' % (r_name)
        else:
            newMovie = Movie(name=r_name,director=defaultDir)
            newMovie.save()
            print 'added %s to database' % (newMovie)
            
        if Critic.objects.filter(name=r_critic).exists():
            print '%s critic already exists in the database!' % (r_critic)
        else:
            newCritic = Critic(name=r_critic,organization=myOrg)
            print newCritic
            newCritic.save()
            print 'added %s from %s to critic database' % (r_critic, 'name_of_organization')
        
        print r_name
        
        mymovie = Movie.objects.get(name=r_name)
        print r_critic
        print myOrg
        mycritic = Critic.objects.get(name=r_critic)
        
        if Reviews.objects.filter(movie=Movie.objects.get(name=r_name),critic=Critic.objects.get(name=r_critic)).exists():
            print 'Review of %s from %s already exists!' % (r_name,r_critic)
        else:
            print 'adding review'
            mymov = Movie.objects.get(name=r_name)
            mycritic = Critic.objects.get(name=r_critic)
            newReview = Reviews(movie=mymov,critic=mycritic,organization=myOrg,review_url=r_link,text = r_text, blurb = r_blurb, thumbsup = r_thumbsup, review_polarity = r_polarity, review_subjectivity = r_subjectivity)
            newReview.save()
        
        
        
        
        
        