import boto3
import logging
import os


def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.getLogger("boto3").setLevel(
        logging.WARNING)  # remove lib log noise
    logging.getLogger("botocore").setLevel(
        logging.WARNING)  # remove lib log noise

    # assume role from the Organization managment account and extract temporary credential
    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn=os.environ['ASSUME_ROLE_ARN'],
        RoleSessionName="cross_acct_lambda"
    )
    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']

    # create service client using the assumed role credentials
    org = boto3.client(
        'organizations',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )

    # invoke 'list_accounts_for_parent' API
    marker = None
    while True:
        paginator = org.get_paginator('list_accounts_for_parent')
        response_iterator = paginator.paginate(
            ParentId=os.environ['ORGANISATION_UNIT_ID'],
            PaginationConfig={
                'MaxItems': 20,
                'PageSize': 20,
                'StartingToken': marker})
        for page in response_iterator:
            accountsInfo = page['Accounts']
            logger.info(accountsInfo)
        try:
            marker = page['NextToken']
        except KeyError:
            break
