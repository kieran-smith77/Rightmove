#! python3
from rightmove_webscraper import RightmoveData
import requests
import boto3
import time
import ddb
import tools
from progress.bar import Bar
import webhooks

ssm = boto3.client('ssm', region_name='eu-west-2')
parameter = ssm.get_parameter(Name='/rightmove/scraper/searches')
search_url = parameter['Parameter']['Value'].split(',')[0]

rm = RightmoveData(search_url)

print(rm.results_count, 'results matched search.')

all_results = []
new_listings = 0

bar = Bar('Processing', max=rm.results_count)
for i in rm.get_results['url']:
    id = int(i.split('/')[-2].replace('#',''))
    if not ddb.exists(id):
        new_listings += 1
        time.sleep(0.5)
        all_results.append(tools.get_property(id))
    bar.next()
bar.finish()

if new_listings:
    print('\n' + str(new_listings) + ' new listings found.')
    webhooks.alert(new_listings)
else:
    print('No new listings found.')

ddb.upload(all_results)
