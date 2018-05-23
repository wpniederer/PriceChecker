import ebay
import discogs
import tweet as twitter
import time
import random


def get_input():
    user_input = []
    while True:
        one_line = input().strip()
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
        quit(1)


def get_switches(line):
    if line[1] == '--discogs':
        discog_switches(line)
    elif line[1] == '--ebay':
        ebay_switches(line)
    elif line[1] == '--help':
        help_switch()
    elif line[1] == '--synopsis':
        synopsis_switch()
    else:
        print("Invalid switch or invalid format for input")
        quit(2)


def getswitch_modifier(line, switch):
    modifer_index = line.index(switch)
    try:
        return line[modifer_index + 1]
    except IndexError:
        print('Incorrect input. Did you forget to give a modifier for max/min/bat/n/etc?')
        quit(3)


def ebay_switches(line):
    query = line[0]
    switch_list = line[2:]
    num_to_print = 30
    condition = 'New'
    max = 20
    min = 10
    located_in = 'North America'
    tweet = False
    bat = False

    for switch in switch_list:
        if switch == '-n':
            num_to_print = int(getswitch_modifier(switch_list, '-n'))
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
        elif switch == '--bat':
            bat = True
            token = str(getswitch_modifier(switch_list, '--bat'))

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
                print(str(rando) + ' is not a valid index, trying again...')

        if relevant_info is None:
            print("Nothing to post to twitter")

        else:
            time.sleep(2)
            print("Posted to twitter, link to post: ")
            twitter.print_tweet_url()

    if bat is True:
        token = token.split('.')
        user_name = token[0]
        hash = token[1]
        print("Username: " + user_name)
        print("Hash: " + hash)


def discog_switches(line):
    query = line[0]
    switch_list = line[2:]
    num_to_print = 59
    tweet = False
    search_results_ep = None
    search_results_album = None
    search_results_ww = None
    search_results_us = None
    search_type = None

    for switch in switch_list:
        if switch == '-n':
            num_to_print = int(getswitch_modifier(switch_list, '-n'))
            if num_to_print >= 60:
                print("A value to print greater than 60 will cause discogs to reject your request. Setting to 50....")
                time.sleep(2)
                num_to_print = 59
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
        elif switch == '--bat':
            bat = True
            token = str(getswitch_modifier(switch_list, '--bat'))

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
        if len(search_results) > 0:
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
                    print(str(rando) + ' is not a valid index, trying again...')

            time.sleep(2)
            print("Posted to twitter, link to post: ")
            twitter.print_tweet_url()
        else:
            print("Nothing to post to twitter")
    if bat is True:
        token = token.split('.')
        user_name = token[0]
        hash = token[1]
        print("Username: " + user_name)
        print("Hash: " + hash)



def help_switch():
    print('\n\nFor Discogs: \n'
            + '--------------------------------------------------------------------------------------------------\n'
            + 'Artist search: artist name --discogs -ep/-album --tweet --bat username.hash\n'
            + '==================================================================================================\n'
            + 'Artist search will find the ablums and/or eps for a given artist.\n'
            + 'Required: discogs switch and either album or ep (or both) switch are required \n'
            + 'Optional: --tweet and --bat username.hash\n'
            + '     --tweet will post some info about the search to twitter\n'
            + '     --bat username.hash currently returns username and hash\n'
            + 'Example search: The Strokes --discogs -album --tweet\n'
            + '=====================================================================================================================\n'
            + 'Vinyl record release search: artist name|album/ep --discogs -rUS/-rWW to search from -n # --tweet --bat username.hash\n'
            + '=====================================================================================================================\n'
            + 'Record release search will find up to 60 releases of a particular album/ep (limit of 60 due to\n'
            + '         discogs api request limiter).\n'
            + 'Required: --discogs and either -rWW or -rUS (but not both!)\n'
            + '     -rWW will search for releases both internationally and in the US\n'
            + '     -rUS will search for releases only in the US\n'
            + 'Optional: -n # and --tweet and --bat username.hash\n'
            + '     -n # sets the number to of results to print\n'
            + '     --tweet will post some info about the search to twitter\n'
            + '     --bat username.hash currently returns username and hash\n'
            + 'Example search: The Strokes|Is This It --discogs -rWW -n 10 --tweet')

    print('\nFor eBay: \n'
          + '--------------------------------------------------------------------------------------------------\n'
          + 'search query --ebay -switches --tweet --bat username.hash\n'
          + '==================================================================================================\n'
          + 'eBay search will search ebay for the given query and filter it based on the given parameters.\n'
          + 'Switches (none are required, I was able to set defaults for the ebay api):\n'
          + '       -n # for number to print (limit of 100 due to api)\n'
          + '       -max # for max price\n'
          + '       -min # for min price\n'
          + '       -used for used vinyls\n'
          + '       -ww for an international search\n'
          + '       --tweet will post some info about the search to twitter\n'
          + '       --bat username.hash currently returns username and hash\n'
          + ' Defaults are 20 for max, 10 for min, 30 to print, search limited to North America, and new\n'
          + 'Example search: Pink Floyd The Wall --ebay -ww -max 1000 --tweet')

    print('\nThings to  Note: \n'
          + '--------------------------------------------------------------------------------------------------\n'
          + 'This program works with two lines, either discogs search or ebay search AND .eot. So it is\n'
          + '       a one line program. You CANNOT search both at once.\n'
          + 'I have caught as many errors as I could find, however it is best to stick to the given format for\n'
          + '       all the searches, and please do not push the limits of the API limiters\n'
          + 'Have fun! I put a lot of work into this project, and I am very proud of it. This actually ended up\n'
          + '       being a prototype for the search function I want to implement on my website (building it\n'
          + '       this summer) and it really helped me get familiar with the APIs I plan to use.\n'
          + '       This is definitely my favorite programming project in my college career, and I actually use\n'
          + '       this program to do quick searches for releases and searching ebay.\n')

    print('\nInfo: \n'
          + '--------------------------------------------------------------------------------------------------\n'
          + 'Version        : 1.0.0\n'
          + 'Dependencies   : ebaysdk - for searching ebay\n'
          + '                 discogs-client - for searching discogs\n'
          + '                 python-twitter - for posting to twitter\n'
          + '                 Python3.6 - I used several functions exclusive to this version of python.\n'
          + '                 There are more dependencies that those three require, but they should be \n'
          + '                   downloaded with the APIs. Look at requirements.txt for a complete list \n'
          + '                   of all the dependencies I needed to run this project.\n'
          + 'Author         : Niederer, Walter \n'
          + 'Contact        : wpniederer@gmail.com\n'
          + 'github         : https://github.com/wpniederer/PriceChecker \n')


def synopsis_switch():
    print('\nSearches either ebay or discogs for relevant info and then posts info related to search to twitter.\n')


user_input = get_input()
if len(user_input) == 1:
    search_from = parse_input(user_input, 0)
    get_switches(search_from)

else:
    print('Invalid input, too many lines')

