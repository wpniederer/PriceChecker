#make input reader for gershman
#import ebay
import discogs
#1st line = where to search from
    #--where to search from, search query,
    # --ebay
        #--used, --new, --max, --min
        # -n for number of results to show
    # --discogs
        # -a (for album search) -r (record release search)
        # -n  +  num: number results to show
#2nd line = where to post to



#search_results = ebay.ebaySearch()
#ebay.printResults()

def getInput():
    user_input = []
    while True:
        one_line = input()
        if (one_line and one_line != '.eot'):
            user_input.append(one_line)
        if (one_line == '.eot'):
            break
    return user_input

def parseInput(input, line_n):
    if (len(input[line_n]) > 0):
        line = input[line_n].split(' ')
        return line
    else:
        print('Invalid line')

def getSwitches(line):
    if (line[1] == '--discogs'):
        discogSwitches(line)
    elif (line[1] == '--ebay'):
        ebaySwitches(line)
    elif (line[1] == '--twitter'):
        twitterSwitches(line)
    elif (line[1] == '--reddit'):
        redditSwitches(line)
    else:
        print("Invalid switch or invalid format for input")

def ebaySwitches(line):
    print()


def discogSwitches(line):
    query = line[0]
    num_to_print = 50
    for switch in line:
        if (switch == '-n'):
            num_to_print = 5
        if (switch == '-a'):
            discogs.discogsArtistSearch(query)
        if (switch == '-r'):
            discogs.discogsRecordSearch(query.split('|'), num_to_print)

def twitterSwitches(line):
    print()

def redditSwitches(line):
    print()

user_input = getInput()
if (len(user_input) == 1):
    search_from = parseInput(user_input, 0)
    print(search_from)
    #getSwitches(search_from)

elif (len(user_input) == 2):
    search_from = parseInput(user_input, 0)
    post_to = parseInput(user_input, 1)

else:
    print('Invalid input, too many lines')
