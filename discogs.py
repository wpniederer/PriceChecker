# consider giving user to search for all releases vs just albums/masters
# fix issue with space as an input
import discogs_client
from discogs_client import exceptions
from itertools import islice
import config
import time

user_agent = ('PriceChecker/1.0' '+https://github.com/wpniederer/PriceChecker')
utoken = config.discogs_user_token
discogsclient = discogs_client.Client(user_agent, user_token=utoken)
sleep_time = 2


def url_builder(discogs_id, r_type):
    url = 'https://www.discogs.com/{type:}/{id:}'.format(type=r_type, id=discogs_id)
    return url


def album_printer(query, search_results):
    print('\n{:=^135}'.format('Albums by ' + query))
    print('{:^90}|{:^45}'.format('Album', 'Link'))
    print('{:-^135}'.format('-'))

    for release in islice(search_results, num_to_print):
        print('{album:90}|'.format(album=release.title), end='')
        print('{url:45}'.format(url=url_builder(release.id, 'master')))
    print('{:-^135}'.format('-'))


def ep_printer(query, search_results):
    print('\n{:=^135}'.format('EPs by ' + query))
    print('{:^90}|{:^45}'.format('EP', 'Link'))
    print('{:-^135}'.format('-'))

    for release in islice(search_results, num_to_print):
        print('{album:90}|'.format(album=release.title), end='')
        print('{url:45}'.format(url=url_builder(release.id, 'master')))
    print('{:-^135}'.format('-'))


def record_printer(query, search_results, num_to_print):
    print('\n{:=^120}'.format('Releases of ' + query[1] + ' by ' + query[0]))
    print('{:^20s}|{:^20s}|{:^14s}|{:^9s}|{:^45s}'
          .format('Artist', 'Album', 'Year', 'Country', 'Link'))
    print('{:-^120}'.format('-'))

    for release in islice(search_results, num_to_print):
        try:
            print('{artist:20}|'.format(artist=', '.join(artist.name for artist in release.artists)), end='')
            print('{album:20}|'.format(album=release.title), end='')
            if (release.year == 0):
                print('{message:^14}|'.format(message='Year not given'), end='')
            else:
                print('{year:^14}|'.format(year=release.year), end='')
            print('{country:^9}|'.format(country=release.country), end='')
            print('{url:45}'.format(url=url_builder(release.id, 'release')))

        except(exceptions.HTTPError):
            user_input2 = input("\nMaxed out number of requests that can be made in a minute...(w)ait or (e)xit: ")
            # user_input2 = 'w'

            if (user_input2 == 'w'):
                print('\nWaiting 61 seconds\n')
                time.sleep(61)

                print('\n{:=^120}'.format('Releases of ' + user_input[1] + ' by ' + user_input[0]))
                print('{:^20s}|{:^20s}|{:^14s}|{:^9s}|{:^45s}'
                      .format('Artist', 'Album', 'Year', 'Country', 'Link'))
                print('{:-^120}'.format('-'))
                continue

            else:
                print('exiting....')
                time.sleep(2)
                break

    print('{:-^120}'.format('-'))


# Artist album/EP search
def discogs_artist_search(user_input):
    # album search
    search_results = discogsclient.search(artist=user_input, type='master', format='album',
                                          sort='title', sort_order='asc')
    if (len(search_results) > 0):
        album_printer(user_input, search_results)

    # EP search
    search_results = discogsclient.search(artist=user_input, type='master', format='EP',
                                          sort='title', sort_order='asc')
    if (len(search_results) > 0):
        ep_printer(user_input, search_results)


# record release search
def discogs_record_search(user_input, num_to_print):
    search_results = discogsclient.search(title=user_input[1], type='release',
                                          artist=user_input[0], format='vinyl', sort='year', sort_order='asc')

    if (len(search_results) == 0):
        print('No results for {} by {}.'.format(user_input[0], user_input[1]))
        time.sleep(2)
        quit()

    elif (len(search_results) > 60):
        print(
            '\n{} by {} has over {} releases, mostly likely due to multiple international releases....limiting search to US'
                .format(user_input[1], user_input[0], len(search_results)))
        time.sleep(sleep_time)
        search_results = discogsclient.search(title=user_input[1], type='release',
                                              artist=user_input[0], format='vinyl', sort='year', sort_order='asc',
                                              country='us')
    record_printer(user_input, search_results, num_to_print)


if __name__ == "__main__":
    num_to_print = 200

    user_input = input(
        "Enter artist and album separated by '|' (artist|album) or just artist to find all albums: ").split('|')

    if (len(user_input) == 1):
        user_input = user_input[0]
        discogs_artist_search(user_input)

    elif (len(user_input) == 2):
        discogs_record_search(user_input, num_to_print)

    else:
        print('\nInvalid Input')
