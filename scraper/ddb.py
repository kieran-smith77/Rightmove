import boto3
import json
from decimal import Decimal
from tinydb import TinyDB, Query


db = TinyDB('../db/db.json')

def upload(records):
    for record in records:
        records[record]['id'] = str(record)
        item = records[record]
        db.insert(item)

def exists(id):
    key = Query()
    item = db.search(key.id == id)
    if item:
        return True
    return False

if __name__ == '__main__':
    upload({1: {'id':1,'value':2},
            2: {'id':2,'review':'Good'},
            3: {'id':3,'review':'Bad'}
            }
        )
    print(exists("1"))
    print(exists("2"))
