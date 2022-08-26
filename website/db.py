from random import randrange
import boto3
import collections
from boto3.dynamodb.conditions import Key
import validators

dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
table = dynamodb.Table("rightmove_table")


def get_new_item(user_id):
    # return first item without review
    response = table.query(
        IndexName="review",
        KeyConditionExpression=Key("review").eq("none") & Key("user").eq(int(user_id)),
    )
    if response["Items"]:
        rn = randrange(len(response["Items"]))
        item = response.get("Items")[rn]
        item["photos"] += item["floorplans"]
        if validators.url(item["url"]):
            return collections.namedtuple("item", item.keys())(*item.values())
    return ""


def get_item(id, user_id):
    # return item by id
    response = table.query(
        KeyConditionExpression=Key("id").eq(int(id)) & Key("user").eq(int(user_id))
    )
    if response["Items"]:
        item = response["Items"][0]
        item["photos"] += item["floorplans"]
        if validators.url(item["url"]):
            return collections.namedtuple("item", item.keys())(*item.values())
    return ""


def get_old_items(user_id, good=None):
    if good is True:
        check = "Good"
    elif good is False:
        check = "Bad"
    else:
        check = None
    if check:
        response = table.query(
            IndexName="review",
            KeyConditionExpression=Key("review").eq(check)
            & Key("user").eq(int(user_id)),
        )
    else:
        response = table.query(
            IndexName="review",
            KeyConditionExpression=Key("review").eq("none")
            & Key("user").eq(int(user_id)),
        )
    if "Items" in response:
        items = response["Items"]
    else:
        items = []

    data = []
    for item in items:
        datum = {
            "id": item["id"],
            "photo": item["photos"][0],
            "address": item["address"].split(",")[0].strip()[:15],
            "url": item["url"],
            "price": item["price"],
            "bedrooms": item["bedrooms"],
        }
        data.append(collections.namedtuple("datum", datum.keys())(*datum.values()))
    return data


def set_review(id, user_id, review):
    # update item with review = review
    if review not in ["Good", "Bad"]:
        return None

    table.update_item(
        Key={"id": int(id), "user": int(user_id)},
        UpdateExpression="SET review = :review",
        ExpressionAttributeValues={":review": review},
    )
    return None


def copy_to_new(id, old_user, new_user, review):
    if review not in ["Good", "Bad"]:
        return None
    old_user = int(old_user)

    item = table.get_item(Key={"id": int(id), "user": int(old_user)})["Item"]
    new_item = item
    new_item["id"] = int(id)
    new_item["user"] = int(new_user)
    table.put_item(Item=new_item)
