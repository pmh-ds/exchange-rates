import boto3
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info('Loading function')


def reformat_json(response):
    # rearrange the response to not be nested
    # i.e. {"rates": {"EUR": 1.2}} -> {"EUR": 1.2}
    rates = response.pop("rates")
    response.update(rates)

    # update response to DynamoDB's required format
    response_updated = {}
    for key, val in response.items():
        # date and base fields are strings (DynamoDB has no date type) whereas everything else is a
        # number
        if key == "date" or key == "base":
            val_type = "S"
        else:
            val_type = "N"
            val = str(val)
        response_updated[key] = {val_type: val}

    return response_updated


def handle(event, context):
    # initialise DynamoDB client
    dynamodb = boto3.client('dynamodb', 'eu-west-2')

    # perform API call
    response = requests.get("http://api.fixer.io/latest?base=GBP")

    # handle bad responses
    if response.status_code == 200:
        logger.info("Request to Fixer successful")
    else:
        logger.info("Response status code {}".format(response.status_code))
        return {"success": False, "status_code": response.status_code}

    # format JSON response into format required by DynamoDB
    response_json = reformat_json(response.json())

    # put item into DynamoDB table
    dynamodb.put_item(TableName="exchange-rates-table",
                      Item=response_json)

    # return successful response
    return {"success": True, "status_code": response.status_code}
