import keys
from ebaysdk.finding import Connection as Finding
from itertools import islice

app_id = keys.ebay_app_id


def search_printer(search, search_results):
    try:
        print('\n{:=^170}'.format('Search results for ' + search))
        for item in search_results['searchResult']['item']:
            print('Title: {}'.format(item['title']))
            print('Price: ${}'.format(item['sellingStatus']['convertedCurrentPrice']['value']))
            print('URL: {}'.format(item['viewItemURL']))
            print('{:-^170}'.format('-'))
    except KeyError:
        print("\n No results for " + search)


def twitter_friendly(rando, search_results):
    try:
        relevant_info = []
        for item in islice(search_results['searchResult']['item'], rando, rando + 1):
            relevant_info.append(item['title'])
            relevant_info.append(item['sellingStatus']['convertedCurrentPrice']['value'])
            relevant_info.append(item['viewItemURL'])
        return relevant_info
    except KeyError:
        return None


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
    max_price = '100'
    min_price = '5'
    condition = 'New'
    num_to_print = '10'
    located_in = 'WorldWide'

    search = input('Search for: ')
    search_results = ebay_search(search, max_price, min_price, condition, num_to_print, located_in)
    search_printer(search, search_results)


