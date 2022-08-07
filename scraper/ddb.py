import boto3
import time
import json
from decimal import Decimal
import tools

dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
table = dynamodb.Table("rightmove_dev_table")
user_table = dynamodb.Table("rightmove_users")


def upload(id, user, search):
    listing = tools.get_property(id)
    listing["review"] = "none"
    listing["user"] = user
    listing["searches"] = [search]
    listing["TimeToLive"] = int(time.time()) + 1209600  # Current Time + 2 weeks
    listing = json.loads(json.dumps(listing), parse_float=Decimal)
    table.put_item(Item=listing)


def update_ttl(item):
    table.update_item(
        Key={"id": item["id"], "user": item["user"]},
        UpdateExpression="SET TimeToLive = :TTL",
        ExpressionAttributeValues={
            ":TTL": int(time.time()) + 1209600
        },  # Current time + two weeks
    )


def add_search(item, search):
    new_searches = item["searches"] + [search]
    table.update_item(
        Key={"id": item["id"], "user": item["user"]},
        UpdateExpression="SET TimeToLive = :TTL, searches = :SEARCHES",
        ExpressionAttributeValues={
            ":TTL": int(time.time()) + 1209600,
            ":SEARCHES": new_searches,
        },  # Current time + two weeks
    )


def exists(id, user, search):
    item = table.get_item(Key={"id": id, "user": user})

    if "Item" not in item:
        upload(id, user, search)
        return False

    item = item["Item"]

    if search in item["searches"]:
        update_ttl(item)
        return True

    add_search(item, search)
    return True


def get_searches():
    searches = []
    items = user_table.scan(ProjectionExpression="userID,searches")["Items"]
    for user in items:
        if "searches" in user:
            searches.append(
                {"userId": int(user["userID"]), "searches": user["searches"]}
            )
    return searches


def get_webhooks(user):
    webhooks = []
    item = user_table.get_item(Key={"userID": user}, ProjectionExpression="webhooks")
    if "Item" not in item:
        return webhooks
    item = item["Item"]
    if "webhooks" in item:
        for hook in item["webhooks"]:
            webhooks.append(hook["link"])
    return webhooks


if __name__ == "__main__":
    # print(exists(124991735, 1, "Sheffield"))
    print(get_webhooks(1))
