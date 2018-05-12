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


def post_to_twitter_discogs_album (info_to_post):
    artist_album = info_to_post[0].split('-')
    artist = artist_album[0]
    artist = artist[:-1]

    album = artist_album[1]
    album = album[1:]
    url = info_to_post[1]
    #num_of_releases = info_to_post[2]
    twitter_client.PostUpdate('Someone searched for ' + artist + '! Here is some info about ' + artist + ':\n'
                              + artist + ' has a release titled ' + album + '\n'
                              + url)


def post_to_twitter_discogs_releases(info_to_post, rando, query):
    query = query.split('|')
    artist = query[0]
    album = query[1]
    year = str(info_to_post[2])
    country = info_to_post[3]
    url = info_to_post[4]
    num_of_releases = str(info_to_post[5])
    #print(info_to_post)

    if (rando == 1):
        twitter_client.PostUpdate(
            'Someone searched for the vinyl record releases of ' + album + ' by ' + artist + '! Here is some info about one of the releases:\n'
            + 'This particular release of ' + album + ' was released in the year ' + year + ' in ' + country + '\n'
            + url)

    if (rando == 2):
        twitter_client.PostUpdate(
            'Someone searched for the vinyl record releases of ' + album + ' by ' + artist + '! Here is some info about the album:\n'
            + album + ' had ' + num_of_releases + ' rereleases.\n'
            + 'Here is a link to one of the releases:\n' + url)


def post_to_twitter_ebay(search, info_to_post):
    title = info_to_post[0]
    price = info_to_post[1]
    url = info_to_post[2]
    twitter_client.PostUpdate('Someone searched for ' + search + '! Here is an eBay listing:\n'
                              + 'Listing Title: ' + title + '\n'
                              + 'Listing Price: $' + price + '\n'
                              + url)
def url_builder(post_id):
    url = 'https://www.twitter.com/{user:}/status/{id:}'.format(user='VinylRecordBot', id=post_id)
    return url

def print_tweet_url():
    statuses = twitter_client.GetHomeTimeline(1)
    status = statuses[0]
    print(url_builder(status.id_str))


#twitter_client.PostUpdate("Bye Miss Chelsea!")


#twitter_client.GetUr
if __name__ == "__main__":
    print("Main")
    print_tweet_url()
