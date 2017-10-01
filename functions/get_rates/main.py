import json
import requests

print('Loading function')


def reformat_json(response):
    rates = response.pop("rates")
    response.update(rates)

    return response


def handle(event, context):
    response = requests.get("http://api.fixer.io/latest?base=GBP")
    print(response.status_code)

    response_json = reformat_json(response.json())

    return response_json
