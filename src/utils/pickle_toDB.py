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

from django.db.models import Q
userdict = {n.name: n for n in TwitterUser.objects.all() }
ntwkdict = {n.name: n for n in Network.objects.all() }
showdict = {n.name: n for n in Show.objects.all() }


def add_df(tablename):
    engine = create_engine('postgresql://sanjeev:Daconia4$@localhost/manatweedb')
    db = pd.read_sql_table(tablename,engine)
    TV_PATH = '/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/utils/picklejar/TV_new.pickle'
    with open(TV_PATH, 'rb') as handle:
        TV = pickle.load(handle)
    if tablename=='twttr_twitteruser':
        TV.username.index = range(len(TV.username))
        userspickles = pd.DataFrame(TV.username.unique(),index=range(len(TV.username.unique())))
        userdb = db.name
        ds1 = set([ tuple(line) for line in userspickles.values.tolist()])
        ds2a = [[x] for x in userdb.values.tolist()]
        ds2 = set([ tuple(line) for line in ds2a])
        ds1.difference(ds2)
        users_add=pd.DataFrame(list(ds1.difference(ds2)))
        if len(users_add) ==0:
            print "False"
        else:
            return users_add
    
    
    if tablename=='twttr_show':
        TV.show.index = range(len(TV.show))
        showpickles = pd.DataFrame(TV.show.unique(),index=range(len(TV.show.unique())))
        showpickles=showpickles[0].apply(lambda x:x.replace('_',' ')).to_frame()
        showdb = db.name
        ds1 = set([ tuple(line) for line in showpickles.values.tolist()])
        ds2a = [[x] for x in showdb.values.tolist()]
        ds2 = set([ tuple(line) for line in ds2a])
        ds1.difference(ds2)
        shows_add=pd.DataFrame(list(ds1.difference(ds2)))
        if len(shows_add)==0:
            print "False"
        else:
            return shows_add
    if tablename=='twttr_network':
        TV.ntwk.index = range(len(TV.ntwk))
        ntwkpickles = pd.DataFrame(TV.ntwk.unique(),index=range(len(TV.ntwk.unique())))
        ntwkpickles=ntwkpickles[0].apply(lambda x:x.replace('_',' ')).apply(lambda x:x.upper()).to_frame()
        ntwkdb = db.name
        ds1 = set([ tuple(line) for line in ntwkpickles.values.tolist()])
        ds2a = [[x] for x in ntwkdb.values.tolist()]
        ds2 = set([ tuple(line) for line in ds2a])
        ds1.difference(ds2)
        ntwk_add=pd.DataFrame(list(ds1.difference(ds2)))

        if len(ntwk_add)==0:
            print "False"
        else:
            return ntwk_add
    
        
    
def InsertUser(df):
    if len(df)>0:
        for i in range(len(df)):
            user = TwitterUser(name=df[0].iloc[i])
            try:
                user.save()
            except:
                print 'inserting user ' + user.name + ' has failed!'
    else:
        return "this has failed, empty dataframe"


def InsertShow(df):
    if len(df)>0:
        for i in range(len(df)):
            show = Show(name=df[0].iloc[i])
            try:
                show.save()
            except:
                print 'inserting show ' + show.name + ' has failed!'
    else:
        return "this has failed, empty dataframe"
    

def InsertNetwork(df):
    if len(df)>0:
        for i in range(len(df)):
            ntwk = Network(name=df[0].iloc[i])
            try:
                ntwk.save()
            except:
                print 'inserting show ' + ntwk.name + ' has failed!'
    else:
        return "this has failed, empty dataframe"

def InsertContent():
    TV_PATH = '/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/utils/picklejar/TV_new.pickle'
    userdict = {n.name: n for n in TwitterUser.objects.all() }
    ntwkdict = {n.name: n for n in Network.objects.all() }
    showdict = {n.name: n for n in Show.objects.all() }
    with open(TV_PATH, 'rb') as handle:
        TVpkl = pickle.load(handle)
    TVdb = pd.read_sql_table('twttr_twittercontent',engine)
    add_TV=TVpkl[TVpkl.datetime>max(TVdb.timeoftweet)]
    print 'adding %f new entries...' % (len(add_TV))
    for i in range(len(add_TV)):
        try:
            tweet = TwitterContent(name=userdict[add_TV.iloc[i].username.replace('_',' ')],show=showdict[add_TV.iloc[i].show.replace('_',' ')],network=ntwkdict[add_TV.iloc[i].ntwk.replace('_',' ').upper()],timeoftweet=add_TV.iloc[i].datetime,sentiment=add_TV.iloc[i].sentiment,text=add_TV.iloc[i].tweet)
            tweet.save()
            if i % 1000 == 0:
                print i
        except:
            print "FAILED: " + add_TV.iloc[i].tweet
        
    
try:
    userdf=add_df('twttr_twitteruser')
except:
    print "failed to query user db"
try:
    showdf=add_df('twttr_show')
except:
    print "failed to query show db"
try:
    ntwkdf = add_df('twttr_network')
except:
    print "failed to query network db"

try:
    InsertUser(userdf)
except:
    print "failed to insert new users"
try:
    InsertShow(showdf)
except:
    print "failed to insert new shows"
try:
    InsertNetwork(ntwkdf)
except:
    print "failed to insert new networks"

try:
    InsertContent()
except:
    print "failed to insert new tweets"