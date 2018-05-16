import discogs_client
from discogs_client import exceptions
from itertools import islice
import keys
import time

user_agent = 'PriceChecker/1.0' '+https://github.com/wpniederer/PriceChecker'
utoken = keys.discogs_user_token
discogsclient = discogs_client.Client(user_agent, user_token=utoken)
sleep_time = 2


def url_builder(discogs_id, r_type):
    url = 'https://www.discogs.com/{type:}/{id:}'.format(type=r_type, id=discogs_id)
    return url


def album_printer(query, search_results):
    print('\n{:=^135}'.format('Albums by ' + query))
    print('{:^90}|{:^45}'.format('Album', 'Link'))
    print('{:-^135}'.format('-'))

    for release in search_results:
        print('{album:90}|'.format(album=release.title), end='')
        print('{url:45}'.format(url=url_builder(release.id, 'master')))
    print('{:-^135}'.format('-'))


def ep_printer(query, search_results):
    print('\n{:=^135}'.format('EPs by ' + query))
    print('{:^90}|{:^45}'.format('EP', 'Link'))
    print('{:-^135}'.format('-'))

    for release in search_results:
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
            if release.year == 0:
                print('{message:^14}|'.format(message='Year not given'), end='')
            else:
                print('{year:^14}|'.format(year=release.year), end='')
            print('{country:^9}|'.format(country=release.country), end='')
            print('{url:45}'.format(url=url_builder(release.id, 'release')))

        except exceptions.HTTPError:
            #user_input2 = input("\nMaxed out number of requests that can be made in a minute...(w)ait or (e)xit: ")
            user_input2 = 'e'

            if user_input2 == 'w':
                print('\nWaiting 61 seconds\n')
                time.sleep(61)

                print('\n{:=^120}'.format('Releases of ' + user_input[1] + ' by ' + user_input[0]))
                print('{:^20s}|{:^20s}|{:^14s}|{:^9s}|{:^45s}'
                      .format('Artist', 'Album', 'Year', 'Country', 'Link'))
                print('{:-^120}'.format('-'))
                continue

            else:
                print('Maxed out number of requests that can be made in a minute, exiting....')
                time.sleep(2)
                break

    print('{:-^120}'.format('-'))


# Artist - album search
def discogs_album_search(user_input):
    # album search
    search_results = discogsclient.search(artist=user_input, type='master', format='album',
                                          sort='title', sort_order='asc')
    return search_results

# Artist - EP search
def discogs_ep_search(user_input):
    search_results = discogsclient.search(artist=user_input, type='master', format='EP',
                                          sort='title', sort_order='asc')
    return search_results


# record release search - international
def discogs_record_search_ww(user_input):
    search_results = discogsclient.search(title=user_input[1], type='release',
                                          artist=user_input[0], format='vinyl', sort='year', sort_order='asc')
    return search_results


# record release search - US
def discogs_record_search_us(user_input):
    search_results = discogsclient.search(title=user_input[1], type='release',
                                          artist=user_input[0], format='vinyl', sort='year', sort_order='asc',
                                          country='us')
    return search_results


def twitter_friendly_release(rando, search_results):
    relevant_info = []

    for release in islice(search_results, rando, rando + 1):
        relevant_info.append((', '.join(artist.name for artist in release.artists)))
        relevant_info.append(release.title)
        if release.year == 0:
            relevant_info.append('NA')
        else:
            relevant_info.append(release.year)
        relevant_info.append(release.country)
        relevant_info.append(url_builder(release.id, 'release'))
    relevant_info.append(len(search_results))

    return relevant_info


def twitter_friendly(rando, search_type, search_results):
    relevant_info = []

    if search_type == 'EP':
        for release in islice(search_results, rando, rando + 1):
            relevant_info.append(release.title)
            relevant_info.append(url_builder(release.id, 'master'))

    if search_type == 'album':
        for release in islice(search_results, rando, rando + 1):
            relevant_info.append(release.title)
            relevant_info.append(url_builder(release.id, 'master'))

    return relevant_info


if __name__ == "__main__":
    num_to_print = 200

    user_input = input("Enter artist and album separated by '|' (artist|album) or just artist to find all albums: ").split('|')

    if len(user_input) == 1:
        user_input = user_input[0]

        search_results = discogs_album_search(user_input)
        if len(search_results) > 0:
            album_printer(user_input, search_results)

        search_results = discogs_ep_search(user_input)
        if len(search_results) > 0:
            ep_printer(user_input, search_results)


    elif len(user_input) == 2:
        search_results = discogs_record_search_ww(user_input, num_to_print)


        if len(search_results) == 0:
            print('No results for {} by {}.'.format(user_input[0], user_input[1]))
            time.sleep(2)
            quit()

        elif len(search_results) > 60:
            print(
                '\n{} by {} has over {} releases, mostly likely due to multiple international releases....limiting search to US'
                    .format(user_input[1], user_input[0], len(search_results)))
            search_results = discogs_record_search_us(user_input, num_to_print)
            time.sleep(sleep_time)
            record_printer(user_input, search_results, num_to_print)

        else:
            record_printer(user_input, search_results, num_to_print)
    else:
        print('\nInvalid Input')
