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


def add_the(country):
    if country == 'US' or country == 'UK':
        country = 'the ' + country
        return country

    else:
        return country


def tweet_discogs_albums(info_to_post):
    artist_album = info_to_post[0].split('-')
    artist = artist_album[0]
    artist = artist[:-1]

    album = artist_album[1]
    album = album[1:]
    url = info_to_post[1]
    twitter_client.PostUpdate('Someone searched for ' + artist + '! Here is some info about the artist:\n'
                               'They have a release titled ' + album + '.\n'
                              + url)


def tweet_discogs_releases(info_to_post, rando, query):
    query = query.split('|')
    artist = query[0]
    album = query[1]
    year = str(info_to_post[2])
    country = info_to_post[3]
    url = info_to_post[4]
    num_of_releases = str(info_to_post[5])

    if rando == 1:
        twitter_client.PostUpdate(
            'Someone searched for the vinyl record releases of ' + album + ' by ' + artist + '! Here is some info about one of the releases:\n'
            + 'This particular release of ' + album + ' was released in the year ' + year + ' in ' + add_the(country) + '\n'
            + url)

    elif rando == 2:
        twitter_client.PostUpdate(
            'Someone searched for the vinyl record releases of ' + album + ' by ' + artist + '! Here is some info about the album:\n'
            + album + ' has ' + num_of_releases + ' rereleases.\n'
            + 'Here is a link to one of the releases:\n' + url)


def tweet_ebay_search(search, info_to_post):
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




if __name__ == "__main__":
    print("Main")
    print_tweet_url()
