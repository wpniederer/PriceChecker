# give link for buying the album
# listing title -- price -- url
import datetime
import config
from ebaysdk.finding import Connection as Finding


app_id = config.app_id
search = 'The Strokes'
max_price = '20'
min_price = '5'
condition = 'New'
num_to_print = '5'


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

for item in search_results['searchResult']['item']:
    #print('ItemID: {}'.format(item['itemId']))
    print('Title: {}'.format(item['title']))
    print('Price: ${}'.format(item['sellingStatus']['currentPrice']['value']))
    print('URL: {}'.format(item['viewItemURL']))
