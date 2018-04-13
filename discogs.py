import discogs_client
import config
from itertools import islice


user_agent = ('PriceChecker/1.0' '+https://github.com/wpniederer/PriceChecker')
utoken = config.discogs_user_token
discogsclient = discogs_client.Client(user_agent, user_token=utoken)
num_to_print = 155
user_input = input("Enter artist and album separated by '|' (artist|album) or just artist to find all albums: ").split('|')

if (len(user_input) == 1):
    # user_input = 'The Strokes'
    user_input = user_input[0]
    search_results = discogsclient.search(artist=user_input, type='master', format='album',
                                          sort='title', sort_order='asc')
    if (len(search_results) == 0 ):
        print('\nCould not find any albums released by ' + user_input + ',searching for all releases(EPs/Singles/Compilations/etc....)')
        search_results = discogsclient.search(artist=user_input, type='release', sort='title', sort_order='asc')

    print('\n{:=^100}'.format('Albums by ' + user_input))
    print('{:^20s}|{:^20s}|'.format('Discogs ID', 'Album'))
    print('{:-^100}'.format('-'))

    for release in islice(search_results, num_to_print):
        print('{id:^20}|'.format(id=release.id), end='')
        print('{album:20}|'.format(album=release.title))
    print('{:-^100}'.format('-'))
    #print(release.link)

elif (len(user_input) == 2):
    # user_input = ['The Strokes','Is This It']
    search_results = discogsclient.search(title=user_input[1], type='release',
        artist=user_input[0], format='LP, album', sort='year', sort_order='asc')

    if (len(search_results) > 60):
        print('\n{} by {} has over {} releases, mostly likely due to multiple international releases....limiting search to US'
                .format(user_input[1], user_input[0], len(search_results)))
        search_results = discogsclient.search(title=user_input[1], type='release',
                                          artist=user_input[0], format='LP, album', sort='year', sort_order='asc', country='us')

    if (len(search_results) == 0):
        print('\n{} by {} has no releases under the album tag, retrying as a general search of LPs'.format(user_input[1], user_input[0]))
        search_results = discogsclient.search(title=user_input[1], type='release',
                                          artist=user_input[0], format='LP', sort='year', sort_order='asc')
        if (len(search_results) == 0):
            print('\n{} by {} has no releases under general search of LPs, retrying as 12in + album'.format(user_input[1], user_input[0]))
            search_results = discogsclient.search(title=user_input[1], type='release',
                                              artist=user_input[0], format='12, album', sort='year', sort_order='asc')
        if (len(search_results) == 0):
            print('\n{} by {} has no releases 12in + album, retrying as general search of 12in'.format(user_input[1], user_input[0]))
            search_results = discogsclient.search(title=user_input[1], type='release',
                                                  artist=user_input[0], format='12', sort='year', sort_order='asc')

    print('\n{:=^100}'.format('Releases of ' + user_input[1] + ' by ' + user_input[0]))
    print('{:^20s}|{:^20s}|{:^20s}|{:^20s}|{:^20s}'.format('Discogs ID', 'Artist', 'Album', 'Year', 'Label'))
    print('{:-^100}'.format('-'))

    for release in islice(search_results, num_to_print):
        print('{id:^20}|'.format(id=release.id), end='')
        print('{artist:20}|'.format(artist=', '.join(artist.name for artist in release.artists)), end='')
        print('{album:20}|'.format(album=release.title), end='')
        if (release.year == 0):
            print('{message:^20}|'.format(message='Year not given'), end='')
        else:
            print('{year:^20}|'.format(year=release.year), end='')
        print('{label:20}'.format(label=', '.join(label.name for label in
                                        release.labels)))
    print('{:-^100}'.format('-'))
else:
    print('\nInvalid Input')


