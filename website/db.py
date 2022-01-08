from tinydb import TinyDB, Query
import collections
import json

try:
    db = TinyDB('/db/db.json')
except FileNotFoundError:
    db = TinyDB('../db/db.json')

def get_new_item():
    obj = Query()
    try:
        item = db.get(~ (obj.review.exists()))
    except json.decoder.JSONDecodeError:
        item = None

    if item:
        item['photos'] += item['floorplans']
        return collections.namedtuple("item", item.keys())(*item.values())
    else:
        return ""

def get_item(id):
    obj = Query()
    try:
        item = db.get(obj.id == id)
    except json.decoder.JSONDecodeError:
        item = None
    if item:
        return collections.namedtuple("item", item.keys())(*item.values())

    else:
        return ""


def get_old_items(good):
    obj = Query()
    if good:
        check = 'Good'
    else:
        check = 'Bad'
    items = db.search(obj.review == check)

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
    print('set')
    if review not in ['Good', 'Bad']:
        return None
    obj = Query()
    db.update({'review': review}, obj.id == id)
    return None
