import ebay
import discogs
import tweet as twitter
import time
import random


def get_input():
    user_input = []
    while True:
        one_line = input()
        if one_line and one_line != '.eot':
            user_input.append(one_line)
        if one_line == '.eot':
            break
    return user_input


def parse_input(input, line_n):
    if len(input[line_n]) > 0:
        line = input[line_n]
        query = line.split('--')
        query_length = len(query[0])
        line = line[query_length:].split(' ')
        line.insert(0, query[0].strip(' '))
        return line
    else:
        print('Invalid line')


def get_switches(line):
    if line[1] == '--discogs':
        discog_switches(line)
    elif line[1] == '--ebay':
        ebay_switches(line)
    elif line[1] == '--help':
        help_switch(line)
    elif line[1] == '--synopsis':
        synopsis_switch(line)
    elif line[1] == '--bat':
        bat_switch(line)
    else:
        print("Invalid switch or invalid format for input")


def getswitch_modifier(line, switch):
    modifer_index = line.index(switch)
    return int(line[modifer_index + 1])


def ebay_switches(line):
    query = line[0]
    switch_list = line[2:]
    num_to_print = 30
    condition = 'New'
    max = 20
    min = 10
    located_in = 'North America'
    tweet = False

    for switch in switch_list:
        if switch == '-n':
            num_to_print = getswitch_modifier(switch_list, '-n')
            # print(num_to_print)
        elif switch == '-used':
            condition = 'Used'
        elif switch == '-max':
            max = getswitch_modifier(switch_list, '-max')
        elif switch == '-min':
            min = getswitch_modifier(switch_list, '-min')
        elif switch == '-ww':
            located_in = 'WorldWide'
        elif switch == '--tweet':
            tweet = True

    search_results = ebay.ebay_search(query, max, min, condition, num_to_print, located_in)
    ebay.search_printer(query, search_results)

    if tweet is True:
        while True:
            try:
                rando = random.randint(0, num_to_print - 1)
                relevant_info = ebay.twitter_friendly(rando, search_results)
                twitter.tweet_ebay_search(query, relevant_info)
                break;

            except IndexError:
                print('invalid index, trying again...')

        time.sleep(2)
        print("Posted to twitter, link: ")
        twitter.print_tweet_url()


def discog_switches(line):
    query = line[0]
    switch_list = line[2:]
    num_to_print = 50
    tweet = False
    search_results_ep = None
    search_results_album = None
    search_results_ww = None
    search_results_us = None
    search_type = None

    for switch in switch_list:
        if switch == '-n':
            num_to_print = getswitch_modifier(switch_list, '-n')
            if num_to_print >= 60:
                print("A value to print greater than 60 will cause discogs to reject your request. Setting to 50....")
                time.sleep(2)
                num_to_print = 50
        elif switch == '-album':
            search_results_album = discogs.discogs_album_search(query)
        elif switch == '-ep':
            search_results_ep = discogs.discogs_ep_search(query)
        elif switch == '-rWW':
            search_results_ww = discogs.discogs_record_search_ww(query.split('|'))
        elif switch == '-rUS':
            search_results_us = discogs.discogs_record_search_us(query.split('|'))
        elif switch == '--tweet':
            tweet = True

    if search_results_album is not None:
        discogs.album_printer(query, search_results_album)
        search_results = search_results_album
        search_type = 'album'

    if search_results_ep is not None:
        discogs.ep_printer(query, search_results_ep)
        search_results = search_results_ep
        search_type = 'EP'

    if search_results_ww is not None:
        discogs.record_printer(query.split('|'), search_results_ww, num_to_print)
        search_results = search_results_ww

    if search_results_us is not None:
        discogs.record_printer(query.split('|'), search_results_us, num_to_print)
        search_results = search_results_us

    if tweet is True:
        while True:
            try:
                if search_type is not None:
                    rando = random.randint(0, len(search_results) - 1)
                    relevant_info = discogs.twitter_friendly(rando, search_type, search_results)
                    twitter.tweet_discogs_albums(relevant_info)
                else:
                    rando = random.randint(0, len(search_results) - 1)
                    relevant_info = discogs.twitter_friendly_release(rando, search_results)
                    rando = random.randint(1, 2)
                    twitter.tweet_discogs_releases(relevant_info, rando, query)
                break

            except IndexError:
                print('invalid index, trying again...')


        time.sleep(2)
        print("Posted to twitter, link to post: ")
        twitter.print_tweet_url()


def help_switch(line):
    print()


def synopsis_switch(line):
    print()


def bat_switch(line):
    print()


user_input = get_input()
if len(user_input) == 1:
    search_from = parse_input(user_input, 0)
    get_switches(search_from)

else:
    print('Invalid input, too many lines')

