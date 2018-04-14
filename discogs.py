import discogs_client
import config
import time
import string
from itertools import islice


user_agent = ('PriceChecker/1.0' '+https://github.com/wpniederer/PriceChecker')
utoken = config.discogs_user_token
discogsclient = discogs_client.Client(user_agent, user_token=utoken)
num_to_print = 155
sleep_time = 2
user_input = input("Enter artist and album separated by '|' (artist|album) or just artist to find all albums: ").split('|')

def urlbuilder(artist_name, discogs_id, r_type):
    translator = str.maketrans('', '', string.punctuation)
    artist_name = artist_name.translate(translator)
    url = 'https://www.discogs.com/{artist:}/{type:}/{id:}'.format(artist=artist_name, type=r_type, id=discogs_id)
    url = url.replace(' ', '-')

    return url


if (len(user_input) == 1):
    # user_input = 'The Strokes'
    user_input = user_input[0]
    search_results = discogsclient.search(artist=user_input, type='master', format='album',
                                          sort='title', sort_order='asc')
    release_type = 'master'

    if (len(search_results) == 1 ):
        print('\nCould not find any albums released by ' + user_input + ',searching for all releases(EPs/Singles/Compilations/etc....)')
        time.sleep(sleep_time)
        search_results = discogsclient.search(artist=user_input, type='release', sort='title', sort_order='asc')
        release_type = 'release'

    print('\n{:=^120}'.format('Albums by ' + user_input))
    print('{:^60}|{:^60}'.format('Album', 'Link'))
    print('{:-^120}'.format('-'))

    for release in islice(search_results, num_to_print):
        #print('{id:^20}|'.format(id=release.id), end='')
        print('{album:60}|'.format(album=release.title), end='')
        print('{url:60}'.format(url=urlbuilder(user_input, release.id, release_type)))
    print('{:-^120}'.format('-'))

elif (len(user_input) == 2):
    # user_input = ['The Strokes','Is This It']
    search_results = discogsclient.search(title=user_input[1], type='release',
        artist=user_input[0], format='vinyl, album', sort='year', sort_order='asc')

    if (len(search_results) > 60):
        print('\n{} by {} has over {} releases, mostly likely due to multiple international releases....limiting search to US'
                .format(user_input[1], user_input[0], len(search_results)))
        time.sleep(sleep_time)
        search_results = discogsclient.search(title=user_input[1], type='release',
                                          artist=user_input[0], format='vinyl, album', sort='year', sort_order='asc', country='us')

    if (len(search_results) == 0):
        print('\n{} by {} has no releases under the album tag, retrying as a general search of records'.format(user_input[1], user_input[0]))
        time.sleep(sleep_time)
        search_results = discogsclient.search(title=user_input[1], type='release',
                                          artist=user_input[0], format='vinyl', sort='year', sort_order='asc')

    print('\n{:=^120}'.format('Releases of ' + user_input[1] + ' by ' + user_input[0]))
    print('{:^20s}|{:^20s}|{:^20s}|{:^20s}|{:^20s}|{:^20s}'
          .format('Discogs ID', 'Artist', 'Album', 'Year', 'Label', 'Country Released'))
    print('{:-^120}'.format('-'))

    for release in islice(search_results, num_to_print):
        #print('{id:^20}|'.format(id=release.id), end='')
        print('{artist:20}|'.format(artist=', '.join(artist.name for artist in release.artists)), end='')
        print('{album:20}|'.format(album=release.title), end='')
        if (release.year == 0):
            print('{message:^20}|'.format(message='Year not given'), end='')
        else:
            print('{year:^20}|'.format(year=release.year), end='')
        print('{label:20}|'.format(label=', '.join(label.name for label in
                                        release.labels)), end='')
        print('{country:^20}'.format(country=release.country))
    print('{:-^120}'.format('-'))
else:
    print('\nInvalid Input')


