from misc_twitter_functions import *
import numpy as np
import scipy as sc
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
import os.path

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

file = open('/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/utils/picklejar/last_run.pickle','rb')
last_run_date = pickle.load(file)
dt = last_run_date.strftime('%Y-%m-%d')

twitter_tv_dict = {
    
    'hbo': {'true_detective': ['#TrueDetective'], 'last_week_tonight': ['#LastWeekTonight'], 'silicon_valley':['#SiliconValleyHBO','#SiliconHBO'],'veep':['#VeepHBO'],'curb_your_enthusiasm':['#CurbYourEnthusiasm'],'real_time':['#RealTime','#RealTimeHBO'],'ballers':['#BallersHBO'],'westworld':['#Westworld','#WestworldHBO'],'insecure':['#InsecureHBO'],'vice_principals':['#VicePrincipals','#VicePrincipalsHBO'],'room_104':['#Room104','#Room104HBO'],'the_comeback':['#TheComeback','#TheComebackHBO'],'the_deuce':['#TheDeuce','#TheDeuceHBO'],'crashing':['#CrashingHBO']},
    
    'nflx': {'house_of_cards':['#HouseofCards'],'narcos':['#Narcos'], 'oitnb':['#OITNB'],'arrested_development':['#ArrestedDevelopment'],'glow':['#GlowNetflix'],'master_of_none':['#MasterOfNone'],'bojack_horseman':['#BojackHorseman'],'sense8':['#Sense8']},

    'amzn': {'man_in_the_high_castle':['#HighCastle'],'transparent':['#TransparentTV'],'mozart_in_the_jungle':['#MozartInTheJungle']},
    
    
    'hulu': {'handmaids_tale':['#HandmaidsTale']},
    
    'got': {'game_of_thrones':['#GameOfThrones']},
    
    'st': {'stranger_things':'#StrangerThings'}
    
}

Sentiment_List_TV = []

twitter_movie_dict = {

    'the_post': ['#ThePost','#ThePostMovie'],
    
    'phantom_thread': ['#PhantomThread'],
    
    'three_billboards': ['#ThreeBillboards'],
    
    'dunkirk': ['#Dunkirk'],
    
    'ladybird':['#LadyBird','Lady Bird'],

    'last_jedi':['#LastJedi'],
    
    'jumanji_welcome_to_the_jungle': ['#JUMANJI'],

    'call_me_by_your_name':['#CallMeByYourName','Call Me By Your Name'],

    'mollys_game':['#MollysGame'],

}


for key in twitter_movie_dict:

    PATH = '/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/movies/'
    filename = key + '_sentiment.csv'
    PATH = PATH + filename
    if os.path.isfile(PATH):
        df = pd.read_csv(PATH,names=['datetime','username','tweet'])
    else:
        print 'csv for %s doesnt exist!' % (key)
        with open(PATH, "w") as my_empty_csv:
              # now you have an empty file already
            pass
        print 'the csv for %s now exists' % (key)


movies = HBO_Twitter_Sentiment(twitter_movie_dict,'movies',dt)    
    
try:
    movies.fetch_tweet_sentiments()
    time.sleep(90)
except:
    print "movies has failed"
    
PATH = '/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/movies/'

file = open('/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/utils/picklejar/TV_new.pickle','rb')
TV_old_obj = pickle.load(file)

for key in twitter_movie_dict:
    PATH = '/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/movies/'
    file = open('/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/utils/picklejar/TV_new.pickle','rb')
    TV_old_obj = pickle.load(file)
    with open('/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/utils/picklejar/TV_old.pickle', 'wb') as handle:
        pickle.dump(TV_old_obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
    filename = key + '_sentiment.csv'
    PATH = PATH + filename
    df = pd.read_csv(PATH,names=['datetime','username','tweet'])
    df.datetime = df.datetime.apply(parser.parse)
    df['show'] = key
    df['ntwk'] = 'movies'
    df['sentiment'] = df.tweet.apply(get_tweet_sentiment)
    df.set_index(df.datetime,inplace=True)
    df.drop_duplicates(inplace=True)
    TV = pd.concat([TV_old_obj,df])
    TV.drop_duplicates(inplace=True)
    with open('/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/site/src/utils/picklejar/TV_new.pickle', 'wb') as handle:
        pickle.dump(TV, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    

    




