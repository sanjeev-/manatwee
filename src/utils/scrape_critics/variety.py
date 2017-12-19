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


varietydict = {}
defaultDir = Director.objects.all()[0]
VAR_URL = 'http://variety.com/v/film/reviews/'
variety_soup = BeautifulSoup(get(VAR_URL).text,'html.parser')
review_list = []
VarietyOrg = Organization.objects.get(name='Variety')
#for noodle in variety_soup.find_all('div',class_='l-river__content')[0].find_all('a')[0].img['alt']
for noodle in variety_soup.find_all('div',class_='l-river__content')[0].find_all('a'):
    if len(noodle.text)>4:
        r_dict = {}
        name = noodle.text
        name=name[13:].replace("'",'')
        if Movie.objects.filter(name=name).exists():
            print '%s movie already exists in the Database' % (name)
        else:
            newMovie = Movie(name=name,director=defaultDir)
            newMovie.save()
            print 'added %s to database' % (newMovie)
        r_url = noodle['href']
        r_dict['link'] = r_url
        r_dict['movie'] = name
        r_soup = BeautifulSoup(get(r_url).text,'html.parser')
        r_author = r_soup.find_all('meta',attrs={'name':'author'})[0]['content']
        if Critic.objects.filter(name=r_author).exists():
            print '%s critic already exists in the database!' % (r_author)
        else:
            newCritic = Critic(name=r_author,organization=VarietyOrg)
            print newCritic
            newCritic.save()
            print 'added %s from %s to critic database' % (r_author, 'variety')
        r_dict['critic'] = r_author
        for beefchunk in r_soup.find_all('meta',attrs={'class':'swiftype'})[0].find_all('meta',attrs={'class':'swiftype'}):
            if len(beefchunk['content'])>140:
                r_text = beefchunk['content']
        r_dict['text'] = r_text
        r_sentiment = TextBlob(r_text).sentiment
        r_polarity = r_sentiment[0]
        r_subjectivity = r_sentiment[1]
        summary = Summarize(name,r_text)
        r_blurb = ' '.join(summary)
        r_dict['review_subjectivity'] = r_subjectivity
        r_dict['review_polarity'] = r_polarity
        r_thumbsup = 'Positive' if r_polarity >0 else 'Negative'
        r_dict['thumbsup'] = r_thumbsup
        r_dict['blurb'] = r_blurb
        if Reviews.objects.filter(movie=Movie.objects.get(name=name),critic=Critic.objects.get(name=r_author,organization=VarietyOrg)).exists():
            print 'Review of %s from %s already exists!' % (name,r_author)
        else:
            print 'adding review'
            mymov = Movie.objects.get(name=name)
            mycritic = Critic.objects.get(name=r_author,organization=VarietyOrg)
            newReview = Reviews(movie=mymov,critic=mycritic,organization=VarietyOrg,review_url=r_url,text = r_text, blurb = r_blurb, thumbsup = r_thumbsup, review_polarity = r_polarity, review_subjectivity = r_subjectivity)
            newReview.save()
        varietydict[name] = r_dict