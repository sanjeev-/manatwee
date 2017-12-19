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

class HBO_Twitter_Sentiment(object):
    #The format of hashtagdict shall be as such:
    # { 'deuce' : [ * a list of all the hashtags to associate with the deuce * ]     }
    # since_date is YYYY-MM-SS , <string>
    # base_folder is e.g. hbo, nflx, huli, or amzn
    
    def __init__(self,mydict,base_folder,since_date):
        #   Twitter API Setup 
        consumer_key = "ZNb0uYLpAN4ADRtrTmY2smhjN"
        consumer_secret = "RtCdA6U9UKASRL8qKWjANlGdownRbtAAWWJf9eAeunLKxcfkRD"
        access_token = "17603883-PI4tf2uJ77IYKNv3Z7eSVJIgskOhj68rhYdL3AfnQ"
        access_token_secret = "JZ6ubUNrT9QN3nxiu8JgjcWk2zTA5aw0qIFx8BioaV7E3"

        auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
        auth.set_access_token(access_token,access_token_secret)
        self.api = tweepy.API(auth)
        self.hashtagdict = mydict
        print self.hashtagdict
        self.base_folder = base_folder
        self.since_date = since_date
    
    def listToQuery(self,hashtag):
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
    
    
    def clean_tweet(self,tweet):

        #Utility function to clean tweet text by removing links, special characters
        #using simple regex statements.
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity == 0:
            return 'Neutral'
        else:
            return 'Negative'
        
    def fetch_tweet_sentiments(self):
        for key in self.hashtagdict:
            time.sleep(90)
            filename = key+'_sentiment.csv'
            path = '/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/'+self.base_folder +'/'+filename
            print path
            query = self.listToQuery(self.hashtagdict[key])
            
            # Open/Create a file to append data
            csvFile = open(path, 'a')
            #Use csv Writer
            csvWriter = csv.writer(csvFile)
            api_query = tweepy.Cursor(self.api.search,q=query,count=500,lang="en",since=self.since_date).items()
            for tweet in api_query:
                print (tweet.created_at, tweet.author._json['screen_name'], tweet.text)
                csvWriter.writerow([tweet.created_at,tweet.author._json['screen_name'],tweet.text.encode('utf-8')])
                
    def generateNetPosDataFrame(self):
        for key in self.hashtagdict:
            filename = key+'_sentiment.csv'
            path = '/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/'+self.base_folder +'/'+filename
            show_df = pd.read_csv(path, names=['datetime','tweet'])
            show_df.dropna(inplace=True)
            show_df['sentiment'] = show_df.tweet.apply(self.get_tweet_sentiment)
            show_df.datetime = show_df.datetime.apply(parser.parse)
            show_df.set_index(show_df.datetime,inplace=True)
            show_grouped = show_df.groupby([pd.TimeGrouper(freq='D'),'sentiment',]).size()
            show_pct = show_grouped.groupby(level=0).apply(lambda x: 100 * x/float(x.sum()))
            show_NNP = show_pct.swaplevel(i=-1,j=-2).sort_values().unstack().transpose()
            show_NNP['NetPositive'] = show_NNP['Positive'] - show_NNP['Negative']
            show_grouped=show_grouped.swaplevel(i=-1,j=-2).sort_values().unstack().transpose()
            show_grouped['TotalTweets'] = show_grouped['Positive'] + show_grouped['Negative'] + show_grouped['Neutral']
            show_NNP['TotalTweets'] = show_grouped['TotalTweets']
            return show_NNP, show_df
        
    def generatePlots(self):
        for key in self.hashtagdict:
            print key
            filename = key+'_sentiment.csv'
            path = '/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/'+self.base_folder +'/'+filename
            show_df = pd.read_csv(path, names=['datetime','username','tweet'])
            show_df.dropna(inplace=True)
            show_df.drop_duplicates(inplace=True)
            show_df['sentiment'] = show_df.tweet.apply(self.get_tweet_sentiment)
            show_df.datetime = show_df.datetime.apply(parser.parse)
            show_df.set_index(show_df.datetime,inplace=True)
            show_grouped = show_df.groupby([pd.TimeGrouper(freq='D'),'sentiment',]).size()
            show_pct = show_grouped.groupby(level=0).apply(lambda x: 100 * x/float(x.sum()))
            show_NNP = show_pct.swaplevel(i=-1,j=-2).sort_values().unstack().transpose()
            if show_NNP.shape[1] <3:
                continue
            if 'Negative' in show_NNP.columns and 'Positive' in show_NNP.columns:
                show_NNP['NetPositive'] = show_NNP['Positive'] - show_NNP['Negative']
            elif 'Negative' in show_NNP.columns:
                show_NNP['NetPositive'] = -show_NNP['Negative']
            elif 'Positive' in show_NNP.columns:
                show_NNP['NetPositive'] = show_NNP['Positive']
            show_grouped=show_grouped.swaplevel(i=-1,j=-2).sort_values().unstack().transpose()
            if 'Negative' in show_NNP.columns and 'Positive' in show_NNP.columns and 'Neutral' in show_NNP.columns:
                show_grouped['TotalTweets'] = show_grouped['Positive'] + show_grouped['Negative'] + show_grouped['Neutral']
            elif 'Negative' in show_NNP.columns and 'Neutral' in show_NNP.columns:
                show_grouped['TotalTweets'] = show_grouped['Negative'] + show_grouped['Neutral']
            elif 'Positive' in show_NNP.columns and 'Neutral' in show_NNP.columns:
                show_grouped['TotalTweets'] = show_grouped['Positive'] + show_grouped['Neutral']
            elif 'Positive' in show_NNP.columns and 'Negative' in show_NNP.columns:
                show_grouped['TotalTweets'] = show_grouped['Positive'] + show_grouped['Negative']
            elif 'Negative' in show_NNP.columns:
                show_grouped['TotalTweets'] = show_grouped['Negative']
            elif 'Positive' in show_NNP.columns:
                show_grouped['TotalTweets'] = show_grouped['Positive']
            elif 'Neutral' in show_NNP.columns:
                show_grouped['TotalTweets'] = show_grouped['Neutral']
            show_NNP['TotalTweets'] = show_grouped['TotalTweets']
            fig_show, ax1_show = plt.subplots()
            ax2_show = ax1_show.twinx()
            if 'NetPositive' in show_NNP.columns:
                ax1_show.plot(show_NNP.NetPositive,'g',linewidth=5)
            ax2_show.bar(show_NNP.index,show_NNP.TotalTweets,align='center',alpha=0.5)
            ax1_show.set_ylim([-100,100])
            ax1_show.set_xlabel('Date')
            ax1_show.set_ylabel('Net Positive Sentiment %')
            ax2_show.set_ylabel('Total Tweets')
            fig_show.autofmt_xdate()
            plt.title(key)
            #fig_show.show()
    
    def tweetDataFrames(self):
        dataframedict = {}
        for key in self.hashtagdict:
            filename = key+'_sentiment.csv'
            path = '/home/ubuntu/cv/aerial/DeepNetsEO/DeepNetsForEO/nlp/' + self.base_folder+ '/'+filename
            show_df = pd.read_csv(path, names=['datetime','username','tweet'])
            show_df.dropna(inplace=True)
            show_df.drop_duplicates(inplace=True)
            show_df['sentiment'] = show_df.tweet.apply(self.get_tweet_sentiment)
            show_df.datetime = show_df.datetime.apply(parser.parse)
            show_df.set_index(show_df.datetime,inplace=True)
            dataframedict[key] = show_df
        for k in dataframedict.keys():
            dataframedict[k]['show'] = k
            dataframedict[k]['ntwk'] = self.base_folder
        df = pd.concat([dataframedict[x] for x in dataframedict.keys()])
        return df