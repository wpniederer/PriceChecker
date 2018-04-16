# consider giving user to search for all releases vs just albums/masters
import discogs_client
from discogs_client import exceptions
from itertools import islice
import config
import time

user_agent = ('PriceChecker/1.0' '+https://github.com/wpniederer/PriceChecker')
utoken = config.discogs_user_token
discogsclient = discogs_client.Client(user_agent, user_token=utoken)
num_to_print = 200
sleep_time = 2
user_input = input("Enter artist and album separated by '|' (artist|album) or just artist to find all albums: ").split('|')

def urlbuilder(discogs_id, r_type):
    url = 'https://www.discogs.com/{type:}/{id:}'.format(type=r_type, id=discogs_id)
    return url

# Artist album search
if (len(user_input) == 1):
    # user_input = 'The Strokes'
    user_input = user_input[0]
    release_type = 'master'

    # album search
    search_results = discogsclient.search(artist=user_input, type='master', format='album',
                                          sort='title', sort_order='asc')

    if (len(search_results) > 0):
        print('\n{:=^135}'.format('Albums by ' + user_input))
        print('{:^90}|{:^45}'.format('Album', 'Link'))
        print('{:-^135}'.format('-'))

        for release in islice(search_results, num_to_print):
            print('{album:90}|'.format(album=release.title), end='')
            print('{url:45}'.format(url=urlbuilder(release.id, release_type)))
        print('{:-^135}'.format('-'))

    # EP search
    search_results = discogsclient.search(artist=user_input, type='master', format='EP',
                                          sort='title', sort_order='asc')

    if (len(search_results) > 0):
        print('\n{:=^135}'.format('EPs by ' + user_input))
        print('{:^90}|{:^45}'.format('EP', 'Link'))
        print('{:-^135}'.format('-'))

        for release in islice(search_results, num_to_print):
            print('{album:90}|'.format(album=release.title), end='')
            print('{url:45}'.format(url=urlbuilder(release.id, release_type)))
        print('{:-^135}'.format('-'))

# record release search
elif (len(user_input) == 2):
    # user_input = ['The Strokes','Is This It']
    release_type = 'release'
    search_results = discogsclient.search(title=user_input[1], type='release',
        artist=user_input[0], format='vinyl', sort='year', sort_order='asc')

    if (len(search_results) == 0):
        print('No results for {} by {}.'.format(user_input[0], user_input[1]))
        quit()

    elif (len(search_results) > 60):
        print('\n{} by {} has over {} releases, mostly likely due to multiple international releases....limiting search to US'
                .format(user_input[1], user_input[0], len(search_results)))
        time.sleep(sleep_time)
        search_results = discogsclient.search(title=user_input[1], type='release',
                                          artist=user_input[0], format='vinyl', sort='year', sort_order='asc', country='us')

    print('\n{:=^120}'.format('Releases of ' + user_input[1] + ' by ' + user_input[0]))
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
            print('{country:^9}|'.format(country=release.country),end='')
            print('{url:45}|'.format(url=urlbuilder(release.id, release_type)))

        except(exceptions.HTTPError):
            user_input2 = input("\nMaxed out number of requests that can be made in a minute...(w)ait or (e)xit: ")
            #user_input2 = 'w'

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

else:
    print('\nInvalid Input')
