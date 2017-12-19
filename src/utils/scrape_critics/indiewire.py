import os, errno, sys
from bs4 import BeautifulSoup
from requests import get
from textblob import TextBlob
import pandas as pd
from pyteaser import Summarize
from django.utils.encoding import smart_str, smart_unicode
from scraper_functions import *

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

def IW():
    IW_URL = 'http://www.indiewire.com/t/reviews/'
    IWSoup = BeautifulSoup(get(IW_URL).text,'html.parser')
    iw_dict = {}
    for entry in IWSoup.find_all('header',class_='entry-header'):
        r_dict = {}
        name_str = entry.text
        name = name_str[2:name_str.find('Review')-2]
        
        r_dict['name'] = name
        link = entry.a['href']
        r_dict['link'] = link
        
        r_soup = BeautifulSoup(get(link).text,'html.parser')
        r_critic = r_soup.find_all('meta',attrs={'name':'author'})[0]['content']
        r_text = r_soup.find_all('meta',attrs={'name':'body'})[0]['content']
        r_sentiment = TextBlob(r_text).sentiment
        r_polarity = r_sentiment[0]
        r_subjectivity = r_sentiment[1]
        summary = Summarize(name,r_text)
        r_blurb = ' '.join(summary)
        r_thumbsup = 'Positive' if r_polarity >0 else 'Negative'
        
        r_dict['critic'] = r_critic
        r_dict['text'] = r_text
        r_dict['blurb'] = r_blurb
        r_dict['review_subjectivity'] = r_subjectivity
        r_dict['review_polarity'] = r_polarity
        r_dict['sentiment'] = r_sentiment
        r_dict['thumbsup'] = r_thumbsup
        
        
        iw_dict[name] = r_dict
        
    return iw_dict

iw = IW()

reviewsDictToDatabase(iw,'IndieWire')
    
    