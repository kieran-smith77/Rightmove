import boto3

def get_secret_key():
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(Name='rightmove/app/secretkey')
    return parameter['Parameter']['Value']
