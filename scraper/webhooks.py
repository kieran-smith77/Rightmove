import requests
import ddb


def alert(user, count):
    webhooks = ddb.get_webhooks(user)
    for webhook in webhooks:
        requests.post(webhook, json={"value1": str(count)})


if __name__ == "__main__":
    print(alert(1, 1))
