import numpy as np
import pickle
import pandas as pd
from sqlalchemy import create_engine
from dateutil import parser
import os, errno, sys

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

def showToNNP(showname):
    engine = create_engine('postgresql://sanjeev:Daconia4$@localhost/manatweedb')
    df = pd.read_sql_table('twttr_twittercontent',engine)
    shows = pd.read_sql_table('twttr_show',engine)
    show_pk = shows[shows.name==showname].id.iloc[0]
    df.set_index(df.timeoftweet,inplace=True)
    grouped = df[df.show_id == show_pk]
    show_grouped = grouped.groupby([pd.TimeGrouper(freq='D'),'sentiment',]).size()
    show_pct = show_grouped.groupby(level=0).apply(lambda x: 100 * x/float(x.sum()))
    show_NNP = show_pct.swaplevel(i=-1,j=-2).sort_values().unstack().transpose()
    show_NNP = show_NNP.fillna(0)
    print show_NNP
    if 'Negative' in show_NNP.columns and 'Positive' in show_NNP.columns:
        show_NNP['NetPositive'] = show_NNP['Positive'] - show_NNP['Negative']
    elif 'Negative' in show_NNP.columns:
        show_NNP['NetPositive'] = -show_NNP['Negative']
    elif 'Positive' in show_NNP.columns:
        show_NNP['NetPositive'] = show_NNP['Positive']
    show_grouped=show_grouped.unstack()
    show_grouped['TotalTweets'] = 0
    show_grouped=show_grouped.fillna(0)
    if 'Positive' in show_NNP.columns:
        show_grouped['TotalTweets'] = show_grouped['TotalTweets'] + show_grouped['Positive']
    if 'Neutral' in show_NNP.columns:
        show_grouped['TotalTweets'] = show_grouped['TotalTweets'] + show_grouped['Neutral']
    if 'Negative' in show_NNP.columns:
        show_grouped['TotalTweets'] = show_grouped['TotalTweets'] + show_grouped['Negative']
    show_NNP['TotalTweets'] = show_grouped['TotalTweets']
    return show_NNP
    
    
def showToCSV(showname):
    pathshowname = showname.replace(' ','_')
    ROOT = '/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/static/content/'
    path = ROOT + pathshowname + '/sentiment_graphs/twitterdata.csv'
    df = showToNNP(showname)
    if os.path.exists(path):
        df.to_csv(path)
    else:
        os.mkdir(os.path.join(ROOT,pathshowname))
        os.mkdir(os.path.join(ROOT+pathshowname,'sentiment_graphs'))
        df.to_csv(path)
        
showlist=[x.name for x in Show.objects.all()]
for show in showlist:
    print show
    try:
        showToCSV(show)
    except:
        print show + "has failed! somethings up"
