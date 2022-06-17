import requests

def alert(count):
    webhooks = []
    try:
        with open('webhooks.txt') as file:
            for line in file:
                webhooks.append(line.strip())
    except FileNotFoundError:
        print('No webhooks found.')
    for webhook in webhooks:
        requests.post(webhook, json={"value1": str(count)})
