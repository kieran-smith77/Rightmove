import boto3
from boto3.dynamodb.conditions import Key
from bcrypt import hashpw, gensalt, checkpw
import random
from password_strength import PasswordStats
from urllib.parse import urlparse

dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")
user_table = dynamodb.Table("rightmove_users")


def verify_user(user, password):
    if len(user) < 3 or len(user) > 20:
        return None
    if len(password) < 8 or len(password) > 200:
        return False
    password = bytes(password, encoding="utf-8")
    response = user_table.query(
        IndexName="username",
        KeyConditionExpression=Key("username").eq(user),
        ProjectionExpression="password, userID",
    )
    if response["Items"]:
        if checkpw(password, bytes(response["Items"][0]["password"], encoding="utf-8")):
            return int(response["Items"][0]["userID"])
        else:
            return False
    else:
        return None


def create_user(user, password, name):
    # Check username isnt taken
    if len(user) < 3 or len(user) > 20:
        return False, "Len"
    if len(password) < 8 or len(password) > 200:
        return False, "PWLen"
    if len(name) < 3 or len(name) > 20:
        return False, "NLen"
    if user_table.query(
        IndexName="username",
        KeyConditionExpression=Key("username").eq(user),
        ProjectionExpression="username",
    )["Items"]:
        return False, "Username"

    # Check password strength
    password_score = PasswordStats(password).strength()
    if password_score < 0.5:
        return False, "Password"

    # Generate User ID
    while True:
        id = random.randint(1, 1000)
        if "Item" not in user_table.get_item(Key={"userID": id}):
            break

    password = hashpw(bytes(password, encoding="utf-8"), gensalt())
    user_table.put_item(
        Item={
            "userID": id,
            "username": user,
            "password": password.decode("utf-8"),
            "name": name,
        }
    )
    return id, "Successful"


def get_user(user_id):
    response = user_table.query(KeyConditionExpression=Key("userID").eq(user_id))
    if not response["Items"]:
        return None
    return response["Items"][0]


def update_search(data, user_id):
    user = user_table.query(KeyConditionExpression=Key("userID").eq(int(user_id)))[
        "Items"
    ]
    if not user:
        return None
    user = user[0]
    for i in range(len(user["searches"])):
        search = user["searches"][i]
        if search["description"] in data.keys():
            if check_url(data[search["description"]], "www.rightmove.co.uk"):
                user["searches"][i]["link"] = data[search["description"]]

            user_table.put_item(Item=user)


def new_search(data, user_id):
    description = data["newSearchName"]
    link = data["newSearchUrl"]
    if not check_url(link, "www.rightmove.co.uk"):
        return None

    user = user_table.query(KeyConditionExpression=Key("userID").eq(int(user_id)))[
        "Items"
    ]
    if user:
        user = user[0]
    else:
        return None
    if "searches" in user:
        searches = user["searches"]
        for search in searches:
            if search["description"] == description:
                return None

        user["searches"].append({"description": description, "link": link})
    else:
        user["searches"] = [{"description": description, "link": link}]
    user_table.put_item(Item=user)


def remove_search(data, user_id):
    user = user_table.query(KeyConditionExpression=Key("userID").eq(int(user_id)))[
        "Items"
    ]
    if user:
        user = user[0]
    else:
        return None

    remove = int(data["remove"]) - 1
    print(remove)
    if "searches" in user:
        del user["searches"][remove]
        user_table.put_item(Item=user)


def update_webhook(data, user_id):
    user = user_table.query(KeyConditionExpression=Key("userID").eq(int(user_id)))[
        "Items"
    ]
    if not user:
        return None
    user = user[0]
    for i in range(len(user["webhooks"])):
        webhook = user["webhooks"][i]
        if webhook["description"] in data.keys():
            if check_url(data[webhook["description"]]):
                user["webhooks"][i]["link"] = data[webhook["description"]]

            user_table.put_item(Item=user)


def new_webhook(data, user_id):
    description = data["newWebhookName"]
    link = data["newWebhookUrl"]
    if not check_url(link):
        return None

    user = user_table.query(KeyConditionExpression=Key("userID").eq(int(user_id)))[
        "Items"
    ]
    if user:
        user = user[0]
    else:
        return None
    if "webhooks" in user:
        webhooks = user["webhooks"]
        for webhook in webhooks:
            if webhook["description"] == description:
                return None

        user["webhooks"].append({"description": description, "link": link})
    else:
        user["webhooks"] = [{"description": description, "link": link}]
    user_table.put_item(Item=user)


def remove_webhook(data, user_id):
    user = user_table.query(KeyConditionExpression=Key("userID").eq(int(user_id)))[
        "Items"
    ]
    if user:
        user = user[0]
    else:
        return None

    remove = int(data["remove"]) - 1
    if "webhooks" in user:
        del user["webhooks"][remove]
        user_table.put_item(Item=user)


def toggle_registration(user_id):
    response = user_table.query(
        KeyConditionExpression=Key("userID").eq(int(user_id)),
        ProjectionExpression="admin",
    )
    if "Items" not in response:
        print("a")
        return None
    if "admin" not in response["Items"][0]:
        print("b")
        return None
    if response["Items"][0]["admin"] != "True":
        print("c")
        return None
    print("authorized")
    ssm = boto3.client("ssm", region_name="eu-west-2")
    parameter = ssm.get_parameter(Name="/rightmove/app/registration")
    if parameter["Parameter"]["Value"] == "True":
        new_value = "False"
    elif parameter["Parameter"]["Value"] == "False":
        new_value = "True"

    ssm.put_parameter(
        Name="/rightmove/app/registration",
        Overwrite=True,
        Value=new_value,
    )


def check_url(url, domain=None):
    result = urlparse(url)
    if domain:
        if result.netloc != domain:
            return False
    return all([result.scheme, result.netloc])
