# make input reader for gershman
import ebay
import discogs


# 1st line = where to search from
# --where to search from, search query,
# --ebay
# -used, -new, -max, -min
# -n for number of results to show
# --discogs
# -a (for album search) -r (record release search)
# -n  +  num: number results to show
# 2nd line = where to post to


# search_results = ebay.ebaySearch()
# ebay.printResults()


def get_input():
    user_input = []
    while True:
        one_line = input()
        if (one_line and one_line != '.eot'):
            user_input.append(one_line)
        # um excuse u
        if (one_line == '.eot'):
            break
    return user_input


def parse_input(input, line_n):
    if (len(input[line_n]) > 0):
        line = input[line_n]
        # print(line)
        query = line.split('--')
        query_length = len(query[0])
        # query.  line[1:].split(' ')
        line = line[query_length:].split(' ')
        line.insert(0, query[0].strip(' '))
        # print(query[0])
        # print(line)
        return line
    else:
        print('Invalid line')


def get_switches(line):
    if (line[1] == '--discogs'):
        discog_switches(line)
    elif (line[1] == '--ebay'):
        ebay_switches(line)
    elif (line[1] == '--twitter'):
        twitter_switches(line)
    elif (line[1] == '--reddit'):
        reddit_switches(line)
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
    # print(switch_list)

    for switch in switch_list:
        if (switch == '-n'):
            num_to_print = getswitch_modifier(switch_list, '-n')
            # print(num_to_print)
        if (switch == '-used'):
            condition = 'Used'
        if (switch == '-max'):
            max = getswitch_modifier(switch_list, '-max')
        if (switch == '-min'):
            min = getswitch_modifier(switch_list, '-min')
        if (switch == '-ww'):
            located_in = 'WorldWide'

    print(num_to_print, condition, max, min, located_in)
    search_results = ebay.ebay_search(query, max, min, condition, num_to_print, located_in)
    ebay.search_printer(query, search_results)


def discog_switches(line):
    query = line[0]
    switch_list = line[2:]
    num_to_print = 50
    # print(switch_list)

    for switch in switch_list:
        if (switch == '-n'):
            num_to_print = getswitch_modifier(switch_list, '-n')
            # print(num_to_print)
        if (switch == '-a'):
            discogs.discogs_artist_search(query)
        if (switch == '-r'):
            discogs.discogs_record_search(query.split('|'), num_to_print)


def twitter_switches(line):
    print()


def reddit_switches(line):
    print()


user_input = get_input()
if (len(user_input) == 1):
    search_from = parse_input(user_input, 0)
    get_switches(search_from)

elif (len(user_input) == 2):
    search_from = parse_input(user_input, 0)
    post_to = parse_input(user_input, 1)

else:
    print('Invalid input, too many lines')
