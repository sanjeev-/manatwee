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


SLATE_URL = 'http://www.slate.com/articles/arts/movies.html'


SlateSoup = BeautifulSoup(get(SLATE_URL).text,'html.parser')

def Slate():
    slate_dict = {}
    for item in SlateSoup.find_all('div',class_="tile long-hed stacked"):
        if 'reviewed' in item.find_all('a')[0]['href']:
            try:
                r_url= item.find_all('a')[0]['href']

                r_soup = BeautifulSoup(get(r_url).text,'html.parser')
                r_title = r_soup.find_all('h1',class_='article__hed')[0].findAll('em')[0].text


                r_title_slug = r_title.lower().replace(' ','-').replace('(','').replace(')','')

                if r_title_slug in r_url:
                    print 'scraping Slate review for %s' % (r_title)
                    r_dict = {}
                    r_text = ''
                    for item in r_soup.find_all('p',class_='slate-paragraph'):
                        r_text += item.text
                    r_sentiment = TextBlob(r_text).sentiment
                    r_polarity = r_sentiment[0]
                    r_subjectivity = r_sentiment[1]
                    summary = Summarize(r_title,r_text)
                    r_blurb = ' '.join(summary)
                    r_thumbsup = 'Positive' if r_polarity >0 else 'Negative'
                    r_critic = r_soup.find_all('meta',attrs={'name':'author'})[0]['content']
                    r_dict['critic'] = r_critic
                    r_dict['text'] = r_text
                    r_dict['name'] = r_title
                    r_dict['link'] = r_url
                    r_dict['blurb'] = r_blurb
                    r_dict['review_subjectivity'] = r_subjectivity
                    r_dict['review_polarity'] = r_polarity
                    r_dict['sentiment'] = r_sentiment
                    r_dict['thumbsup'] = r_thumbsup
                    slate_dict[r_title] = r_dict 


            except:
                print 'movie not found. skipping...'
        
    return slate_dict

slate = Slate()

reviewsDictToDatabase(slate,'Slate')

        
