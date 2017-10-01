import boto3
import requests

print('Loading function')


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
    print(response.status_code)

    response_json = reformat_json(response.json())

    dynamodb.put_item(TableName="exchange-rates-table",
                      Item=response_json)

    return response_json
