import os, errno, sys
from bs4 import BeautifulSoup
from requests import get
from textblob import TextBlob
import pandas as pd
from pyteaser import Summarize

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

NYTOrg = Organization.objects.get(name='NYT')
def scrapeNYTMovie():
    review_dict = {}
    url = 'https://www.nytimes.com/reviews/movies'
    html_soup=BeautifulSoup(get(url).text,'html.parser')
    movie_length = len(html_soup.find_all('a',class_='story-link'))
    print movie_length
    for i in range(movie_length):
        souplet = html_soup.find_all('a',class_='story-link')[i]
        r_url = 'https://www.nytimes.com/'+souplet['href']
        r_name = souplet.h2.text.strip()
        r_get = get(r_url)
        r_soup = BeautifulSoup(r_get.text,'html.parser')
        review_text = ""
        chunk_count = len(r_soup.find_all('p',class_='story-body-text story-content'))
        author = r_soup.find_all('meta',attrs={"name":"author"})[0]['content']
        for i in range(chunk_count):
            review_text += r_soup.find_all('p',class_='story-body-text story-content')[i].text
        review_sentiment = TextBlob(review_text).sentiment
        review_polarity=review_sentiment[0]
        review_subjectivity=review_sentiment[1]
        r_thumbsup= 'Positive' if review_polarity > 0 else 'Negative'
        summary = Summarize(r_name,review_text)
        r_blurb = ' '.join(summary)
        review_dict[souplet.h2.text.strip()] = {'thumbsup':r_thumbsup,'blurb':r_blurb,'name':r_name,'link':r_url,'text':review_text,'review_subjectivity':review_subjectivity,'critic':author,'organization':'NYT','review_polarity':review_polarity}
    return review_dict


filldirector = Director.objects.all()[0]
NYTOrg = Organization.objects.get(name='NYT')
def dictToDB(moviedict):
    for key in moviedict:
        if Critic.objects.filter(name=moviedict[key]['critic'],organization=NYTOrg).exists():
            print '%s already exists! '% moviedict[key]['critic']
        else:
            newCritic = Critic(name=moviedict[key]['critic'],organization=NYTOrg)
            print 'saving critic %s to DB' % moviedict[key]['critic']
            newCritic.save()
        if Movie.objects.filter(name=moviedict[key]['name']).exists():
            print '%s already exists!' % moviedict[key]['name']
        else:
            newMovie = Movie(name=moviedict[key]['name'],director = filldirector)
            newMovie.save()
            print 'saving movie %s to DB' % moviedict[key]['name']
        if Reviews.objects.filter(movie=Movie.objects.get(name=moviedict[key]['name']),organization=NYTOrg).exists():
            print 'review of %s from %s already exists!' % (moviedict[key]['name'], NYTOrg)
        else:
            newReview = Reviews(movie=Movie.objects.get(name=moviedict[key]['name']),organization=NYTOrg,critic=Critic.objects.get(name=moviedict[key]['critic']),thumbsup=moviedict[key]['thumbsup'],review_polarity=moviedict[key]['review_polarity'],review_subjectivity=moviedict[key]['review_subjectivity'],review_url=moviedict[key]['link'],blurb=moviedict[key]['blurb'],text=moviedict[key]['text'])
            print 'saving new Review of %s from %s' % (moviedict[key]['name'],moviedict[key]['organization'])
            newReview.save()
            

Dict = scrapeNYTMovie()
dictToDB(Dict)