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

CHI_URL = 'http://www.chicagotribune.com/entertainment/movies/'

CHISoup = BeautifulSoup(get(CHI_URL).text,'html.parser')
chi_dict = {}

def ChicagoScraper():
    chi={}
    for x in CHISoup.find_all('div',class_='trb_brk_gc_i'):
        title = x.find_all('a')[0].find_all('figure')[0].find_all('img')[0]['title']
        if 'review:' in title:
            r_dict = {}
            r_url = CHI_URL + x.find_all('a')[0]['href']
            title = str(title[:title.find('review')]).replace("'","").strip()
            r_soup = BeautifulSoup(get(r_url).text,'html.parser')
            r_critic = r_soup.find_all('meta',attrs={'name':'author'})[0]['content']
            r_text = ''
            for piece in r_soup.find_all('div',class_='trb_ar_page')[0].find_all('p'):
                r_text += piece.text
            r_sentiment = TextBlob(r_text).sentiment
            r_polarity = r_sentiment[0]
            r_subjectivity = r_sentiment[1]
            summary = Summarize(title,r_text)
            r_blurb = ' '.join(summary)
            r_thumbsup = 'Positive' if r_polarity >0 else 'Negative'
            print title + ": " + str(r_polarity)
            r_dict['critic'] = r_critic
            r_dict['text'] = r_text
            r_dict['blurb'] = r_blurb
            r_dict['review_subjectivity'] = r_subjectivity
            r_dict['review_polarity'] = r_polarity
            r_dict['sentiment'] = r_sentiment
            r_dict['thumbsup'] = r_thumbsup
            r_dict['name'] = title
            r_dict['link'] = r_url
            chi[title]=r_dict
    return chi

chi = ChicagoScraper()

reviewsDictToDatabase(chi,'ChicagoTribune')