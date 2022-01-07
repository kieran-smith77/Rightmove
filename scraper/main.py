#! /bin/python3
from rightmove_webscraper import RightmoveData
import requests
import time
import ddb
import tools
from progress.bar import Bar


# Get the initial data
url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94124&insId=1&radius=3.0&minPrice=200000&maxPrice=325000&minBedrooms=2&maxBedrooms=4&displayPropertyType=houses&maxDaysSinceAdded=&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false"
rm = RightmoveData(url)

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
