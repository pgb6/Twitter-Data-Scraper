"""
This python file serves as a command line script that will allow the user to
store a users' most recent 100 tweets into an NDJSON file. It can also search
the first 100 tweets with a specified hashtag and display associated distinct hashtags as
well as the count of each distinct hashtag. For information on how to run this
script, please refer to the README.txt
"""
import argparse
import json
import tweepy
import hidden
import sys
import pandas as pd
import collections
import os


class TwitterSearch():
    #get command line args
    def get_args(self):
        # use argparse parser for command line input
        parser = argparse.ArgumentParser(description='Choose which Twitter search(es) to conduct')
        parser.add_argument('-t', '--timeline', type=str,
                            help='Stores the users 100 most recent tweets into a newline-delimited JSON file in CWD. Specify user after flag.')
        parser.add_argument('-H', '--hashtag', type=str,
                            help='Prints dataframe of hashtags and their occurences found in the first 100 results of a Twitter Hashtag search. Also prints dataframe to csv file in CWD. Specify desired hashtag after flag.')

        args = parser.parse_args()
        return args

    #make logs_folder
    def logs_folder(self):
        return os.getcwd()+'/logs/'

    #authenticate
    def API(self):
        auth = hidden.oauth()
        API = tweepy.API(auth, wait_on_rate_limit=True)

        return API

    #Write newline-delimited json of users last 100 tweets
    def user_timeline(self,user):
        API = self.API()
        numTweets = 100
        newline = ''

    #write each tweet and its data into a newline-delimited json formatted file
        with open(self.logs_folder()+'data.json','w+', encoding='utf-8') as out:
            for tweet in tweepy.Cursor(API.user_timeline, screen_name=user, tweet_mode='extended').items(numTweets):
                data = json.dumps(tweet._json,ensure_ascii=False)
                out.write(newline)
                out.write(data)
                newline = '\n'

    #Print hashtags and the number of their occurences in the first 100 tweets with specified hashtag
    def search_hashtag(self, hashtag):
        #filter out retweets in our search, ref: https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators
        search_hashtag = f'#{hashtag} -filter:retweets'
        client = self.API()
        numTweets = 100
        #make an integer default dict of hashtag:occurences, this way any new hashtags will have a default of 0 occurences
        distinct_hashtags = collections.defaultdict(int)
        #iterate through 100 tweets with the hashtag and make the distinct_hashtag dictionary
        for tweet in tweepy.Cursor(client.search, q=search_hashtag, tweet_mode='extended').items(numTweets):
                data = tweet._json['entities']['hashtags']

                for i in range(len(data)):
                    distinct_hashtags[data[i]['text']] += 1

        #make a beautiful pandas dataframe using the distinct_hashtags dict. Printing to the screen will not be perfect due to possible non-Latin hashtags
        hashtag_df = pd.DataFrame(distinct_hashtags.items(),columns=['Hashtag','Occurences'])
        hashtag_df = hashtag_df.sort_values('Hashtag')
        #disable max_rows limit so that the df output is not shorted with ellipsis
        pd.set_option('display.max_rows',None)
        #convert df to csv file, allowing non-Latin hashtags to be seen and analyzed
        if not os.path.exists(self.logs_folder()+'hashtag_df.csv'):
            with open(self.logs_folder()+'hashtag_df.csv', 'w+'): pass
        hashtag_df.to_csv(self.logs_folder()+'hashtag_df.csv',encoding='utf-8-sig', index=False)
        print(hashtag_df.to_string(index=False))


if __name__ == '__main__':
    api = TwitterSearch()
    args = api.get_args()

    #check if any argument(s) present on command line, if its present, run the associated function!
    if args.timeline:
        try:
            api.user_timeline(args.timeline)
            print('JSON file made in logs folder!')
        except tweepy.error.TweepError:
            sys.exit('OAuth Failed!')
    if args.hashtag:
        try:
            api.search_hashtag(args.hashtag)
        except tweepy.error.TweepError:
            sys.exit('OAuth Failed!')

    if not args.timeline and not args.hashtag:
        print('ERROR! Please read the README.md or use -h argument for help.')
