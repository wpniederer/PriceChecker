# give link for buying the album
# listing title -- price -- url
import datetime
import config
import time
from ebaysdk.finding import Connection as Finding


app_id = config.app_id
search = 'The Strokes'
max_price = '20'
min_price = '5'
condition = 'New'
num_to_print = '50'


try:
    ebay_client = Finding(siteid='EBAY-US', appid=app_id, config_file=None)
    ebay_client.execute('findItemsAdvanced', {
        'keywords': search,
        'categoryId': 176985,
        'itemFilter': [
            {'name': 'MaxPrice', 'value': max_price, 'paramName': 'Currency', 'paramValue': 'USD'},
            {'name': 'MinPrice', 'value': min_price, 'paramName': 'Currency', 'paramValue': 'USD'},
            {'name': 'AuctionWithBIN'},
            {'name': 'Condition', 'value': condition},
            {'name': 'HideDuplicateItems', 'value': 'true'}
        ],
        'paginationInput': {
            'entriesPerPage': num_to_print,
            'pageNumber': '1'
        },
        'sortOrder': 'CurrentPriceHighest'
    })
except ConnectionError as e:
    print(e)

search_results = ebay_client.response.dict()
###Need to figure out how to prevent searches with no results#####
#if(len(search_results['searchResult']) == 0):
#if(search_results['searchResult']):
    #print('\nNo search results for {}, now exiting...'.format(search))
    #time.sleep(2)
    #quit()

#else:
print('\n{:=^170}'.format('Search results for ' + search))
#print('{:^8}|{:^70}|{:^90}'.format('Price', 'Title','URL'))
#print('{:=^170}'.format('='))

for item in search_results['searchResult']['item']:
    print('Title: {:70}'.format(item['title']))
    print('Price: ${:8}'.format(item['sellingStatus']['currentPrice']['value']))
    print('URL: {:90}'.format(item['viewItemURL']))
    print('{:-^170}'.format('-'))
