from random import randrange
import boto3
import collections
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
table = dynamodb.Table('rightmove_table')

def get_new_item():
    # return first item without review 
    response = table.query(
        IndexName='review',
        KeyConditionExpression=Key('review').eq("none")
    )
    if response["Items"]:
        rn = randrange(len(response["Items"]))
        item = response.get('Items')[rn]
        item['photos'] += item['floorplans']
        return collections.namedtuple("item", item.keys())(*item.values())
    else:
        return ""

def get_item(id):
    # return item by id
    response = table.query(
        KeyConditionExpression=Key('id').eq(int(id))
    )

    if "Items" in response:
        item = response['Items'][0]
        return collections.namedtuple("item", item.keys())(*item.values())
    else:
        return ""


def get_old_items(good=None):
    # Scan ddb for items where review = good
    if good == True:
        check = 'Good'
    elif good == False:
        check = 'Bad'
    else:
        check = None
    if check:
        response = table.query(
            IndexName='review',
            KeyConditionExpression=Key('review').eq(check)
        )
    else:
        response = table.query(
            IndexName='review',
            KeyConditionExpression=Key('review').eq('none')
        )
    if "Items" in response:
        print(response)
        items = response['Items']
    else:
        print(response) 
        items = [] 

    data = []
    for item in items:
        datum = {
            'id': item['id'],
            'photo': item['photos'][0],
            'address': item['address'].split(',')[0].strip()[:15],
            'url': item['url'],
            'price': item['price'],
            'bedrooms': item['bedrooms']
        }
        data.append(collections.namedtuple("datum", datum.keys())(*datum.values()))
    return data

def set_review(id, review):
    # update item with review = review
    if review not in ['Good', 'Bad']:
        return None
    
    table.update_item(
        Key={'id': int(id)},
        UpdateExpression="SET review = :review",
        ExpressionAttributeValues={":review": review},
    )
    return None
