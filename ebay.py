import config
from ebaysdk.finding import Connection as Finding
from itertools import islice

app_id = config.ebay_app_id


def search_printer(search, search_results):
    print('\n{:=^170}'.format('Search results for ' + search))

    for item in search_results['searchResult']['item']:
        print('Title: {:70}'.format(item['title']))
        print('Price: ${:8}'.format(item['sellingStatus']['currentPrice']['value']))
        print('URL: {:90}'.format(item['viewItemURL']))
        print('{:-^170}'.format('-'))


def ebay_friendly(search_results):
    relevant_info = []
    for item in islice(search_results['searchResult']['item'], 1):
        relevant_info.append(item['title'])
        relevant_info.append(item['sellingStatus']['currentPrice']['value'])
        relevant_info.append(item['viewItemURL'])
    return relevant_info
    #print(relevant_info)


def ebay_search(search, max_price, min_price, condition, num_to_print, located_in):
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
                {'name': 'HideDuplicateItems', 'value': 'true'},
                {'name': 'LocatedIn', 'value': located_in}
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
    return search_results


if __name__ == "__main__":
    max_price = '20'
    min_price = '5'
    condition = 'New'
    num_to_print = '10'
    located_in = 'North America'

    search = input('Search for: ')
    search_results = ebay_search(search, max_price, min_price, condition, num_to_print, located_in)
    search_printer(search, search_results)

    #ebay_friendly(search, search_results)

