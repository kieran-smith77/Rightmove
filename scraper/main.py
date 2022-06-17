#! /bin/python3
from rightmove_webscraper import RightmoveData
import requests
import time
import ddb
import tools
from progress.bar import Bar


# Copy the desired search term from the rightmove website to this variable below 
with open("search.txt") as file:
    search_url = file.read().strip()
rm = RightmoveData(search_url)

print(rm.results_count, 'results matched search.')

all_results = {}

bar = Bar('Processing', max=rm.results_count)
for i in rm.get_results['url']:
    id = i.split('/')[-2].replace('#','')
    if not ddb.exists(id):
        all_results[id] = tools.get_property(id)
    time.sleep(0.5)
    bar.next()
bar.finish()

ddb.upload(all_results)
