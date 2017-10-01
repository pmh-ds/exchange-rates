import json
import requests
from decimal import Decimal

print('Loading function')


def reformat_json(response):
    rates = response.pop("rates")
    response.pop("base")
    response.update(rates)
    response_updated = {}
    for key, val in response.items():
        if key == "date":
            val_type = "S"
        else:
            val_type = "N"
            val = Decimal(str(val))
        response_updated[key] = {val_type: val}

    return response_updated


def handle(event, context):
    response = requests.get("http://api.fixer.io/latest?base=GBP")
    print(response.status_code)

    response_json = reformat_json(response.json())

    return response_json
