import requests
import boto3

def alert(count):
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name='/rightmove/scraper/webhooks')
    webhooks = parameter['Parameter']['Value'].split(',')
    for webhook in webhooks:
        requests.post(webhook, json={"value1": str(count)})
