#! python3
import ddb
import time
import webhooks
import pandas as pd
from tqdm import tqdm
from rightmove_webscraper import RightmoveData

searches = ddb.get_searches()

final_df = None

for user in searches:
    userId = user["userId"]
    links = user["searches"]
    for search in links:
        search_description = search["description"]
        search_url = search["link"]

        rm = RightmoveData(search_url)
        print(rm.results_count, "results matched search.")

        rm = rm.get_results["url"]
        rm = pd.DataFrame(
            {"url": rm.values, "userId": userId, "search": search_description}
        )

        if final_df is None:
            final_df = rm
        else:
            final_df = pd.concat([final_df, rm])

new_listings = {}
rm = final_df

for index, listing in tqdm(rm.iterrows(), total=len(rm)):
    id = int(listing["url"].split("/")[-2].replace("#", ""))
    user = listing["userId"]
    search = listing["search"]

    if not ddb.exists(id, user, search):
        try:
            new_listings[user] += 1
        except KeyError:
            new_listings[user] = 1
    time.sleep(0.5)

for user, count in new_listings.items():
    print(f"\n{count} new listings found for user ID: {user}")
    webhooks.alert(user, count)
