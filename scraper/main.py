#! /bin/python3
from rightmove_webscraper import RightmoveData
import boto3
import time
import ddb
import tools
from progress.bar import Bar
import webhooks

ssm = boto3.client('ssm')
search_url = client.get_parameter(
    Name='search_url',
    WithDecryption=False
).strip()

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

s3 = boto3.client('s3')
with open("/db/db.json", "rb") as f:
    s3.upload_fileobj(f, "kieran-smith-rightmove-db", "db.json")
