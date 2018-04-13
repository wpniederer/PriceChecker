import datetime
import config
from ebaysdk.finding import Connection as Finding


app_id = config.app_id
artist = 'The Strokes'
max_price = '20'
min_price = '5'
condition = 'New'
num_to_print = '25'


ebay_client = Finding(siteid='EBAY-US', appid=app_id, config_file=None)
ebay_client.execute('findItemsAdvanced', {
    'keywords': artist,
    'categoryId': 176985,
    'itemFilter': [
        {'name': 'MaxPrice', 'value': max_price, 'paramName': 'Currency', 'paramValue': 'USD'},
        {'name': 'MinPrice', 'value': min_price, 'paramName': 'Currency', 'paramValue': 'USD'},
        {'name': 'Condition', 'value': condition},
    ],
    'paginationInput': {
        'entriesPerPage': num_to_print,
        'pageNumber': '1'
    },
    'sortOrder': 'CurrentPriceHighest'
})

search = ebay_client.response.dict()

for item in search['searchResult']['item']:
    print('ItemID: {}'.format(item['itemId']))
    print('Title: {}'.format(item['title']))

