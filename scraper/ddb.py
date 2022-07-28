import boto3
import time
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('rightmove_table')


def upload(records):
    with table.batch_writer() as batch:
        for record in records:
            record['scraped_date']=int(time.time())
            record = json.loads(json.dumps(record), parse_float=Decimal)
            batch.put_item(Item=record)

def exists(id):
    item = table.get_item(
        Key={"id": id}
    )
    if 'Item' in item:
        return True
    return False

if __name__ == '__main__':
    # upload([
    #         {'id':10101010,'value':2},
    #         {'id':20202020,'review':'Good'},
    #         {'id':30303030,'review':'Bad'}
    #     ])
    print(exists(1))
    print(exists(9090909))
