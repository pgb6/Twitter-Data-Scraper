import tweepy

def oauth():
    #keys given through developer.twitter.com
    consumer_key = "2KfJrtULz8i2dcwjAdPd2MvHn"
    consumer_secret =  "OSFRvlh0qX6wtlJ5IF65VuYr8m887udZhW3q1ZT5WAHfQLgsHC"
    access_token = "1182428690518437888-JHIh86GBoODvTBIVrxV6ndMJ2fTen9"
    access_secret = "kPWEwgpYMmnwTC4dU5hW1Q2FlmKyx79RUn07h5HKqaqP7"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    return auth
