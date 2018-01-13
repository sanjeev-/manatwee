import numpy as np
import scipy as sc
import os
import sys
import pandas as pd
import csv
import matplotlib.pyplot as plt 
import seaborn as sns
import pickle
import tweepy
import re
from textblob import TextBlob
from dateutil import parser
import seaborn as sns
import time
from datetime import timedelta
from datetime import datetime

file = open('/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/utils/picklejar/last_run.pickle','rb')
last_run_date = pickle.load(file)


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

#   Twitter API Setup 
consumer_key = "ZNb0uYLpAN4ADRtrTmY2smhjN"
consumer_secret = "RtCdA6U9UKASRL8qKWjANlGdownRbtAAWWJf9eAeunLKxcfkRD"
access_token = "17603883-PI4tf2uJ77IYKNv3Z7eSVJIgskOhj68rhYdL3AfnQ"
access_token_secret = "JZ6ubUNrT9QN3nxiu8JgjcWk2zTA5aw0qIFx8BioaV7E3"

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

file = open('/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/utils/picklejar/last_run.pickle','rb')
last_run_date = pickle.load(file)

since_date = last_run_date.strftime('%Y-%m-%d')


television_dict = {
    
'game of thrones':['#GameOfThrones'],
'stranger things':['#StrangerThings'],
'house of cards':['#HouseofCards'],
'westworld':['#Westworld'],
'insecure':['#InsecureHBO'],
'the deuce':['#TheDeuce','#TheDeuceHBO'],
'true detective':['#TrueDetective'],
'bojack horseman':['#BojackHorseman'],
'master of none':['#MasterOfNone'],
'transparent':['#TransparentTV'],
'handmaids tale':['#HandmaidsTale'],

}


movie_dict = {

    'the post': ['#ThePost','#ThePostMovie'],
    'phantom thread': ['#PhantomThread'],
    'three billboards': ['#ThreeBillboards'],
    'dunkirk': ['#Dunkirk'],
    'ladybird':['#LadyBird','Lady Bird'],
    'star wars the last jedi':['#LastJedi'],
    'jumanji welcome to the jungle': ['#JUMANJI'],
    'call me by your name':['#CallMeByYourName','Call Me By Your Name'],
    'mollys game':['#MollysGame'],
    'all the money in the world':['All The Money In The World'],
    'the greatest showman':['#TheGreatestShowman'],
    'pitch perfect 3':['#PitchPerfect3','#PitchPerfect'],

}




show_network_map = {
    
    'game of thrones': 'hbo',
    'stranger things': 'nflx',
    'house of cards': 'nflx',
    'westworld':'hbo',
    'insecure':'hbo',
    'the deuce':'hbo',
    'true detective':'hbo',
    'bojack horseman':'nflx',
    'master of none':'nflx',
    'transparent':'amzn',
    'handmaids tale':'hulu',
    
}

def listToQuery(hashtag):
    if len(hashtag) == 1:
        query = hashtag[0]
    if len(hashtag)>1:
        query = ""
        for i,item in enumerate(hashtag):
            if i == len(hashtag)-1:
                query = query+item
            else:    
                query = query + item + " OR "
    return query

def addUser(tweet):
    username = tweet.author._json['screen_name']
    if TwitterUser.objects.filter(name=username).exists():
        print 'user exists'
    else:
        print 'user %s doesnt exist, creating user...' % (username)
        myUser = TwitterUser(name=username)
        myUser.save()

def checkShowsAndNetworks(show_dict):
    for key in show_dict:
        show_name = key.replace('_',' ').lower()
        if Show.objects.filter(name=show_name).exists():
            print 'show %s already exists' % (show_name)
        else:
            ntwk_name = show_network_map[key]
            if Network.objects.filter(name=ntwk_name).exists():
                print 'the %s network that is affiliated with %s already exists, just need to add show' % (ntwk_name,show_name)
                myNetwork = Network.objects.get(name=ntwk_name.upper())
                myShow = Show(name=show_name,network=myNetwork)
                print 'adding show %s' % (show_name)
                myShow.save()
            else:
                myNetwork = Network(name=ntwk_name.upper())
                print 'adding network %s' % (ntwk_name)
                myNetwork.save()
                myShow = Show(name=show_name,network=myNetwork)
                print 'adding show %s' % (show_name)
                myShow.save()
        
        

def clean_tweet(tweet):

    #Utility function to clean tweet text by removing links, special characters
    #using simple regex statements.
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def get_tweet_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'
    

    
def addTweetToDB(tweet, show):
    username = tweet.author._json['screen_name']
    myNetwork = show.network
    myText = tweet.text.encode('utf-8')
    myText = clean_tweet(myText)
    
    myUser = TwitterUser.objects.get(name=username)
    myShow = show
    mySentiment = get_tweet_sentiment(myText)
    
    myTime = tweet.created_at
    
    myTweet = TwitterContent(name=myUser,text=myText,network=myNetwork,show=myShow,timeoftweet=myTime,sentiment=mySentiment)
    print 'adding Tweet... %s' % (myTweet)
    myTweet.save()
    

def pullfromTwitter(keyword_dict):
    for key in keyword_dict:
        print key
        i=0
        show = Show.objects.get(name=key)
        query = listToQuery(keyword_dict[key])
        query = query + " exclude:retweets"
        twitter_pull = tweepy.Cursor(api.search,q=query,count=100,lang="en").items()
        for tweet in twitter_pull:
            i+=1
            addUser(tweet)
            addTweetToDB(tweet,show)
            if i>1000:
                print '1000 tweets for %s added' % (show.name)
                break

movie_network = Network.objects.get(name='MOVIES')
                
def MoviecheckShowsAndNetworks(show_dict):
    for key in show_dict:
        show_name = key.replace('_',' ').lower()
        if Show.objects.filter(name=show_name).exists():
            print 'show %s already exists' % (show_name)
        else:
            ntwk_name = movie_network
            myShow = Show(name=show_name,network=ntwk_name)
            print 'adding movie %s' % (show_name)
            myShow.save()
             
print 'checking and adding movie models'
MoviecheckShowsAndNetworks(movie_dict)
                
print 'adding tv'
#pullfromTwitter(television_dict)

#time.sleep(900)
print 'adding movies'
pullfromTwitter(movie_dict)
