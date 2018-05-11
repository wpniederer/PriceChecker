import twitter
import config

#for just artist:
    # startmessage: Someone searched for 'artist'!
    # start + did you know that 'artist' released num_of_albums  albums
        # and num_of_eps EPS
    # start + did you know that 'artist' has an EP titled ep_title
    # same as above, except with album
# for artist/album:
    # startmessage: Someone searched for 'album/EP title" by 'artist'!
    # start + did you know that 'title' had over num_of_releases releases internationally
    # start + same as above, but with US
    #


c_key = config.twitter_consumer_key
c_secret = config.twitter_consumer_secret
t_key = config.twitter_token_key
t_secret = config.twitter_token_secret

twitter_client = twitter.Api(consumer_key=c_key,
                           consumer_secret=c_secret,
                           access_token_key=t_key,
                           access_token_secret=t_secret)


def post_to_twitter(artist, message, album):
    try:
        if (album is None):
            twitter_client.PostUpdate("Did message")
        elif (album is not None):
            twitter_client.PostUpdate()
        else:
            print("Error related to album is none")
    except:
        print("Error in posting to VinylRecordBot twitter")


def post_to_twitter(search, info_to_post):
    title = info_to_post[0]
    price = info_to_post[1]
    url = info_to_post[2]
    twitter_client.PostUpdate('Someone searched for ' + search + '! Here is an eBay listing:\n'
                              + 'Title: ' + title + '\n'
                              + 'Price: ' + price + '\n'
                              + 'URL: ' + url)

#twitter_client.PostUpdate("Bye Miss Chelsea!")


if __name__ == "__main__":
    print("Main")
