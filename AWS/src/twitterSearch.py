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
import time
import boto3


class TwitterSearch:
    def get_args(self):
        """get command line args"""

        parser = argparse.ArgumentParser(description='Choose which Twitter search(es) to conduct')
        parser.add_argument('-t', '--timeline', type=str,
                            help='Stores the users 100 most recent tweets into a newline-delimited JSON file in CWD. '
                                 'Specify user after flag.')
        parser.add_argument('-H', '--hashtag', type=str,
                            help='Prints dataframe of hashtags and their occurences found in the first 100 results of '
                                 'a Twitter Hashtag search. Also prints dataframe to csv file in CWD. Specify desired '
                                 'hashtag after flag.')
        parser.add_argument('-b', '--bucket', type=str, help='Choose which AWS S3 bucket to upload the output files')
        args = parser.parse_args()
        return args

    def get_timestamp(self):
        """get timestamp for output file distinction"""

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        return timestamp

    def logs_folder(self):
        """make logs_folder"""

        path = os.getcwd() + '/logs/'
        if not os.path.exists(path):
            os.mkdir(os.getcwd() + '/logs/')
        return path

    def API(self):
        """authenticate with keys"""

        auth = hidden.oauth()
        API = tweepy.API(auth, wait_on_rate_limit=True)

        return API

    def user_timeline(self, user, bucket):
        """Write newline-delimited json of users last 100 tweets"""

        API = self.API()
        numTweets = 100
        newline = ''
        # write each tweet and its data into a newline-delimited json formatted file
        tweets_file = self.logs_folder() + f'{user}_tweets_{self.get_timestamp()}.json'
        if not os.path.exists(tweets_file):
            with open(tweets_file, 'w+'): pass
        with open(tweets_file, 'w+', encoding='utf-8') as out:
            for tweet in tweepy.Cursor(API.user_timeline, screen_name=user, tweet_mode='extended').items(numTweets):
                data = json.dumps(tweet._json, ensure_ascii=False)
                out.write(newline)
                out.write(data)
                newline = '\n'
        self.upload_s3(tweets_file, bucket)

    def search_hashtag(self, hashtag, bucket):
        """Print hashtags and the number of their occurences in the first 100 tweets with specified hashtag"""

        # filter out retweets in our search, ref:
        # https://developer.twitter.com/en/docs/twitter-api/v1/rules-and-filtering/search-operators
        search_hashtag = f'#{hashtag} -filter:retweets'
        client = self.API()
        numTweets = 100
        distinct_hashtags = collections.defaultdict(int)
        # iterate through 100 tweets with the hashtag and make the distinct_hashtag dictionary
        for tweet in tweepy.Cursor(client.search, q=search_hashtag, tweet_mode='extended').items(numTweets):
            data = tweet._json['entities']['hashtags']

            for i in range(len(data)):
                distinct_hashtags[data[i]['text']] += 1

        # make a beautiful pandas dataframe using the distinct_hashtags dict. Printing to the screen will not be
        # perfect due to possible non-Latin hashtags
        hashtag_df = pd.DataFrame(distinct_hashtags.items(), columns=['Hashtag', 'Occurences'])
        hashtag_df = hashtag_df.sort_values('Hashtag')
        pd.set_option('display.max_rows', None)

        # convert df to csv file, allowing non-Latin hashtags to be seen and analyzed
        hashtag_file = self.logs_folder() + f'{hashtag}_hashtag_{self.get_timestamp()}.csv'
        if not os.path.exists(hashtag_file):
            with open(hashtag_file, 'w+'): pass
        hashtag_df.to_csv(hashtag_file, encoding='utf-8-sig',
                          index=False)
        self.upload_s3(hashtag_file, bucket)

    def upload_s3(self, file, bucket):
        """Upload the file to s3 bucket"""
        s3 = boto3.client('s3')
        s3.upload_file(file, bucket, file)

    def main(self):
        """main function"""

        args = self.get_args()

        # check if any argument(s) present on command line, if its present, run the associated function!
        if args.timeline:
            try:
                api.user_timeline(args.timeline, args.bucket)
                print('Tweets JSON uploaded!!')
            except tweepy.error.TweepError:
                sys.exit('OAuth Failed!')
        if args.hashtag:
            try:
                api.search_hashtag(args.hashtag, args.bucket)
                print('Hashtag CSV uploaded!')
            except tweepy.error.TweepError:
                sys.exit('OAuth Failed!')

        if not args.timeline and not args.hashtag:
            print('ERROR! Please read the README.md or use -h argument for help.')


if __name__ == '__main__':
    api = TwitterSearch()
    api.main()
