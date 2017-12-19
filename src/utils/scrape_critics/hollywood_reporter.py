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

defaultDir = Director.objects.all()[0]
HWRorg = Organization.objects.get(name='The Hollywood Reporter')
reviews_toadd= []
rtext_list=[]
def scrapeHWR():
    HWR_URL = 'https://www.hollywoodreporter.com/topic/movie-reviews'
    hwr_soup =BeautifulSoup(get(HWR_URL).text,'html.parser')
    hwr_dict={}
    for noodle in hwr_soup.find_all('a',class_='topic-card__link'):
        a=smart_str(noodle['title']).replace("'",'')
        a=a[:a.find(': Film Review')]
        hwr_dict[a]=noodle['href']
    for key in hwr_dict:
        if Movie.objects.filter(name=key).exists():
            print '%s already exists' % (key)
        else:
            print '%s ...adding this movie' % (key)
            newMovie = Movie(name=key,director=defaultDir)
            newMovie.save()
    for key in hwr_dict:
        review_soup = BeautifulSoup(get(hwr_dict[key]).text,'html.parser')
        r_author=review_soup.find_all('meta',attrs={"name":"sailthru.author"})[0]['content']
        if Critic.objects.filter(name=r_author).exists():
            print '%s already exists!' % (r_author)
        else:
            newCritic = Critic(name=r_author,organization=HWRorg)
            print 'adding %s' % (newCritic)
            newCritic.save()
        review_text = ""
        for item in review_soup.find_all('p',style='margin-bottom: 0in;'):
            review_text +=item.text
        if len(review_text) == 0:
            for item in review_soup.find_all('p'):
                review_text += item.text
        review_sentiment = TextBlob(review_text).sentiment
        summary = Summarize(key,review_text)
        r_blurb = ' '.join(summary)
        #print r_blurb
        rtext_list.append(review_text)
        r_subjectivity = review_sentiment[1]
        r_polarity = review_sentiment[0]
        r_thumbsup = 'Positive' if r_polarity>0 else 'Negative'
        r_url = hwr_dict[key]
        newReviews = Reviews(movie=Movie.objects.get(name=key),review_url=r_url,review_polarity=r_polarity,review_subjectivity=r_subjectivity,thumbsup=r_thumbsup,blurb=r_blurb,text=review_text,critic=Critic.objects.get(name=r_author),organization=HWRorg)
        if Reviews.objects.filter(movie=Movie.objects.get(name=key),organization=HWRorg).exists():
            print 'This review of %s already exists' % (key)
        else:
            print 'adding review'
            reviews_toadd.append(newReviews)
            newReviews.save()
        

scrapeHWR()
        
            
    