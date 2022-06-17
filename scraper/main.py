#! /bin/python3
from rightmove_webscraper import RightmoveData
import requests
import time
import ddb
import tools
from progress.bar import Bar
import webhooks

# Copy the desired search term from the rightmove website to this variable below 
with open("search.txt") as file:
    search_url = file.read().strip()
rm = RightmoveData(search_url)

print(rm.results_count, 'results matched search.')

all_results = {}
new_listings = 0

bar = Bar('Processing', max=rm.results_count)
for i in rm.get_results['url']:
    id = i.split('/')[-2].replace('#','')
    if not ddb.exists(id):
        new_listings += 1
        all_results[id] = tools.get_property(id)
    time.sleep(0.5)
    bar.next()
bar.finish()

if new_listings:
    print('\n' + str(new_listings) + ' new listings found.')
    webhooks.alert(new_listings)
else:
    print('No new listings found.')

ddb.upload(all_results)
