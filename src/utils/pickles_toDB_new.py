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
from critic.models import *

from django.db.models import Q
userdict = {n.name: n for n in TwitterUser.objects.all() }
ntwkdict = {n.name: n for n in Network.objects.all() }
showdict = {n.name: n for n in Show.objects.all() }

TV_PATH = '/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/utils/picklejar/TV_new.pickle'
TV_PATH_old = '/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/utils/picklejar/TV_old.pickle'
with open(TV_PATH, 'rb') as handle:
    newTV = pickle.load(handle)
with open(TV_PATH_old, 'rb') as handle:
    oldTV = pickle.load(handle)

datefile = 'utils/picklejar/last_run.pickle'
last_run_dt =  pickle.load(open(datefile)).strftime('%Y-%m-%d')
    
addTV=newTV[newTV.datetime>=last_run_dt]
print addTV.head()

for user in addTV.username.unique():
    if TwitterUser.objects.filter(name=user).exists():
        a=0
    else:
        addUser = TwitterUser(name=user)
        addUser.save()
        print 'user %s added' % (user)
for ntwk in addTV.ntwk.unique():
    ntwk = ntwk.upper()
    if Network.objects.filter(name=ntwk).exists():
        a=0
    else:
        ntwk = ntwk.upper()
        addNtwk = Network(name=ntwk)
        addNtwk.save()
        print 'network %s added' % (ntwk)
for show in addTV.show.unique():
    show = show.replace('_',' ')
    if Show.objects.filter(name=show).exists():
        a=0
    else:
        print addTV.show
        show = show.replace('_',' ')
        if addTV[addTV.show==show.replace(' ','_')].ntwk[0].upper() == 'MOVIES':
            addShow = Show(name=show, network=Network.objects.filter(name=addTV[addTV.show==show.replace(' ','_')].ntwk[0].upper())[0],category='movie')
        else:
            addShow = Show(name=show, network=Network.objects.filter(name=addTV[addTV.show==show.replace(' ','_')].ntwk[0].upper())[0])
        addShow.save()    
        print 'show %s added' % (show)
        
userdict = {n.name: n for n in TwitterUser.objects.all() }
ntwkdict = {n.name: n for n in Network.objects.all() }
showdict = {n.name: n for n in Show.objects.all() }
        
        
for i in range(len(addTV)):
    try:
        newTweet = TwitterContent(name=userdict[addTV.iloc[i].username],show=showdict[addTV.iloc[i].show.replace('_',' ')],network=ntwkdict[addTV.iloc[i].ntwk.upper()],timeoftweet=addTV.iloc[i].datetime,sentiment=addTV.iloc[i].sentiment,text=addTV.iloc[i].tweet)
        if i % 1000 == 0:
            print i
        print newTweet
        newTweet.save()
    except:
        '%s has failed' % (i)
