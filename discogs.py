import discogs_client
import config
from itertools import islice
import sys


user_agent = ('PriceChecker/0.1' '+https://github.com/wpniederer/PriceChecker')
utoken = config.user_token
discogsclient = discogs_client.Client(user_agent, user_token=utoken)

#user_input = input("Enter artist and album separated by '|' (artist|album): ").split('|')

user_input = ['The Strokes','Is This It']
search_results = discogsclient.search(user_input[1], type='release',
        artist=user_input[0], format='album, LP')

num_to_print = 3
#print ('\n== Search results for {album} by {artist} =='.format(artist=user_input[0], album=user_input[1]))
#for release in islice(search_results, num_to_print):
#    print ('\n\t== discogs-id {id} =='.format(id=release.id))
#    print (u'\tArtist\t: {artist}'.format(artist=', '.join(artist.name for artist
#                                         in release.artists)))
#    print (u'\tAlbum\t: {title}'.format(title=release.title))
#    print (u'\tYear\t: {year}'.format(year=release.year))
#    print (u'\tLabels\t: {label}'.format(label=','.join(label.name for label in
#                                        release.labels)))

print('\n{:^20s}|{:^20s}|{:^20s}|{:^20s}'.format('Artist', 'Album', 'Year', 'Label'))
print('{:-^80}'.format('-'))
for release in islice(search_results, num_to_print):
    print('{artist:20}|'.format(artist=', '.join(artist.name for artist in release.artists)), end='')
    print('{album:20}|'.format(album=release.title), end='')
    print('{year:^20}|'.format(year=release.year), end='')
    print('{label:20}'.format(label=', '.join(label.name for label in
                                        release.labels)))
print('{:-^80}'.format('-'))
    #print('{:10s}, {:10s}, {:10s}, {label:10s}'.format(release.artists, release.title, release.year))
                                                   #label=', '.join(label.name for label in release.labels)))
    #print('\n')
