import discogs_client
import config
from itertools import islice


user_agent = ('PriceChecker/0.1' '+https://github.com/wpniederer/PriceChecker')
utoken = config.user_token
discogsclient = discogs_client.Client(user_agent, user_token=utoken)
num_to_print = 30

user_input = input("Enter artist and album separated by '|' (artist|album) or just artist to find all albums: ").split('|')

if (len(user_input) == 1):
    # user_input = 'The Strokes'
    user_input = user_input[0]
    search_results = discogsclient.search(artist=user_input, type='master', format='album')

    print('\n{:=^100}'.format('Albums by ' + user_input))
    print('{:^20s}|{:^20s}|'.format('Discogs ID', 'Album'))
    print('{:-^100}'.format('-'))

    for release in islice(search_results, num_to_print):
        print('{id:^20}|'.format(id=release.id), end='')
        print('{album:20}|'.format(album=release.title))
    print('{:-^100}'.format('-'))

elif (len(user_input) == 2):
    # user_input = ['The Strokes','Is This It']
    search_results = discogsclient.search(user_input[1], type='release',
        artist=user_input[0], format='album, LP')

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


