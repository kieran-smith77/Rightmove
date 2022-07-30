import boto3

def get_secret_key():
    ssm = boto3.client('ssm', region_name='eu-west-2')
    parameter = ssm.get_parameter(Name='/rightmove/app/secretkey')
    return parameter['Parameter']['Value']

def enable_registration():
    try:
        ssm = boto3.client('ssm', region_name='eu-west-2')
        parameter = ssm.get_parameter(Name='/rightmove/app/registration')
        if parameter['Parameter']['Value'] == 'True':
            return True
        return False

    except: return False