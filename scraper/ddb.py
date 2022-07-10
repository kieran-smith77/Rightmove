from tinydb import TinyDB, Query
import boto3
from os import makedirs, path

filename = '/db/db.json'
makedirs(path.dirname(filename), exist_ok=True)

s3 = boto3.client('s3')
with open(filename, "wb") as f:
    s3.download_fileobj("kieran-smith-rightmove-db", "db.json", f)

db = TinyDB(filename)


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
