import boto3
import json
from decimal import Decimal
from tinydb import TinyDB, Query


db = TinyDB('../db.json')

# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('rm_properties')

def upload(records):
    # with table.batch_writer() as batch:
    #     for record in records:
    #         records[record]['id'] = str(record)
    #         item = json.loads(json.dumps(records[record]), parse_float=Decimal)
    #         batch.put_item(Item=item)

    for record in records:
        records[record]['id'] = str(record)
        item = records[record]
        db.insert(item)

def exists(id):
    # item = table.get_item(Key={'id': str(id)},AttributesToGet=['id',])
    # if 'Item' in item:
    #     return True
    # return False
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
