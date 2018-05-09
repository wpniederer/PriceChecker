import twitter
import config

c_key = config.twitter_consumer_key
c_secret = config.twitter_consumer_secret
t_key = config.twitter_token_key
t_secret = config.twitter_token_secret

twitter_client = twitter.Api(consumer_key=c_key,
                           consumer_secret=c_secret,
                           access_token_key=t_key,
                           access_token_secret=t_secret)


def post_to_twitter(message):
    try:
        twitter_client.PostUpdate(message)
    except:
        print("Error in posting to VinylRecordBot twitter")
