import datetime
import ebaysdk
import config

app_id = config.app_id

ebay_client = ebaysdk.finding(appid=app_id, config_file=None)
response = ebay_client.execute('findItemsAdvanced', {'keywords': 'Python'})
