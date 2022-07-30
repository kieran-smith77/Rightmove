import boto3
from boto3.dynamodb.conditions import Key
from bcrypt import hashpw, gensalt, checkpw
import random
from password_strength import PasswordStats

dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
user_table = dynamodb.Table('rightmove_users')


def verify_user(user,password):
    if len(user) < 3 or len(user) > 20:
        return None
    if len(password) < 8 or len(password) > 200:
        return False
    password=bytes(password, encoding='utf-8')
    response = user_table.query(
        IndexName='username',
        KeyConditionExpression=Key('username').eq(user),
        ProjectionExpression='password, userID',
    )
    if response['Items']:
        if checkpw(password, bytes(response['Items'][0]['password'],encoding='utf-8')):
            return int(response['Items'][0]['userID'])
        else:
            return False
    else:
        return None

def create_user(user,password,name):
    # Check username isnt taken
    if len(user) < 3 or len(user) > 20:
        return False, "Len"
    if len(password) < 8 or len(password) > 200:
        return False, "PWLen"
    if len(name) < 3 or len(name) > 20:
        return False, "NLen"
    if user_table.query(
        IndexName='username',
        KeyConditionExpression=Key('username').eq(user),
        ProjectionExpression='username'
    )['Items']:
        return False, "Username"

    # Check password strength
    password_score = PasswordStats(password).strength()
    if password_score < 0.5:
        return False, "Password"

    # Generate User ID
    while True:
        id = random.randint(1,1000)
        if 'Item' not in user_table.get_item(Key={'userID': id}):
            break

    password=hashpw(bytes(password, encoding='utf-8'),gensalt())
    user_table.put_item(
            Item={'userID':id,'username':user,'password':password.decode("utf-8"), 'name':name}
    )
    return id, "Successful"