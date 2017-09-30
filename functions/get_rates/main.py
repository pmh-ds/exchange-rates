import json
import requests

print('Loading function')


def handle(event, context):
    response = requests.get("http://api.fixer.io/latest?base=GBP")
    print(response.status_code)
    return response.json()
