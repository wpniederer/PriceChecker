import discogs_client
import sys


user_agent = 'PriceChecker/0.1'
discogsclient = discogs_client.Client(user_agent, user_token='')

user_input = input("Enter artist and max price desired").split(' ')


search_results = discogsclient.search('House For All', type='release',
        artist='Blunted Dummies')

print ('\n== Search results for release_title=House For All ==')
for release in search_results:
    print ('\n\t== discogs-id {id} =='.format(id=release.id))
    print (u'\tArtist\t: {artist}'.format(artist=', '.join(artist.name for artist
                                         in release.artists)))
    print (u'\tTitle\t: {title}'.format(title=release.title))
    print (u'\tYear\t: {year}'.format(year=release.year))
    print (u'\tLabels\t: {label}'.format(label=','.join(label.name for label in
                                        release.labels)))
