import boto3
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info('Loading function')


def reformat_json(response):
    rates = response.pop("rates")
    response.update(rates)
    response_updated = {}
    for key, val in response.items():
        if key == "date" or key == "base":
            val_type = "S"
        else:
            val_type = "N"
            val = str(val)
        response_updated[key] = {val_type: val}

    return response_updated


def handle(event, context):
    dynamodb = boto3.client('dynamodb', 'eu-west-2')

    response = requests.get("http://api.fixer.io/latest?base=GBP")
    if response.status_code == 200:
        logger.info("Request to Fixer successful")
    else:
        logger.info("Response status code {}".format(response.status_code))
        return {"success": False, "status_code": response.status_code}

    response_json = reformat_json(response.json())

    dynamodb.put_item(TableName="exchange-rates-table",
                      Item=response_json)

    return {"success": True, "status_code": response.status_code}
