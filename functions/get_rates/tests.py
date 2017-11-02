from unittest import TestCase, mock
import boto3
from botocore.stub import Stubber

from main import reformat_json, handle

TEST_RESPONSE = {
    "base": "GBP",
    "date": "2017-10-26",
    "rates": {
        "AUD": 1.7131,
        "BGN": 2.1973,
        "BRL": 4.2726,
        "CAD": 1.6898,
        "CHF": 1.312,
        "CNY": 8.7634,
        "CZK": 28.748,
        "DKK": 8.3622,
        "HKD": 10.302,
        "HRK": 8.4434,
        "HUF": 348.63,
        "IDR": 17955,
        "ILS": 4.6448,
        "INR": 85.642,
        "JPY": 150.26,
        "KRW": 1483.4,
        "MXN": 25.13,
        "MYR": 5.5906,
        "NOK": 10.658,
        "NZD": 1.9232,
        "PHP": 68.463,
        "PLN": 4.7579,
        "RON": 5.166,
        "RUB": 76.126,
        "SEK": 10.922,
        "SGD": 1.7987,
        "THB": 43.785,
        "TRY": 4.9812,
        "USD": 1.3204,
        "ZAR": 18.806,
        "EUR": 1.1235
    }
}

TEST_RESPONSE_REFORMATTED = {
    "base": {"S": "GBP"},
    "date": {"S": "2017-10-26"},
    "AUD": {"N": "1.7131"},
    "BGN": {"N": "2.1973"},
    "BRL": {"N": "4.2726"},
    "CAD": {"N": "1.6898"},
    "CHF": {"N": "1.312"},
    "CNY": {"N": "8.7634"},
    "CZK": {"N": "28.748"},
    "DKK": {"N": "8.3622"},
    "HKD": {"N": "10.302"},
    "HRK": {"N": "8.4434"},
    "HUF": {"N": "348.63"},
    "IDR": {"N": "17955"},
    "ILS": {"N": "4.6448"},
    "INR": {"N": "85.642"},
    "JPY": {"N": "150.26"},
    "KRW": {"N": "1483.4"},
    "MXN": {"N": "25.13"},
    "MYR": {"N": "5.5906"},
    "NOK": {"N": "10.658"},
    "NZD": {"N": "1.9232"},
    "PHP": {"N": "68.463"},
    "PLN": {"N": "4.7579"},
    "RON": {"N": "5.166"},
    "RUB": {"N": "76.126"},
    "SEK": {"N": "10.922"},
    "SGD": {"N": "1.7987"},
    "THB": {"N": "43.785"},
    "TRY": {"N": "4.9812"},
    "USD": {"N": "1.3204"},
    "ZAR": {"N": "18.806"},
    "EUR": {"N": "1.1235"}
}


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == "http://api.fixer.io/latest?base=GBP":
        return MockResponse(TEST_RESPONSE, 200)

    return MockResponse(None, 404)


class TestClass(TestCase):

    def setUp(self):
        self.test_response = TEST_RESPONSE
        self.test_response_reformatted = TEST_RESPONSE_REFORMATTED

    def test_reformat_json(self):
        print(self.test_response)
        test_response_rates = self.test_response["rates"]
        test_response_updated = reformat_json(self.test_response)
        self.assertEqual(test_response_updated["base"], {
                         "S": self.test_response["base"]})
        self.assertEqual(test_response_updated["date"], {
                         "S": self.test_response["date"]})
        self.assertEqual(test_response_updated["AUD"], {
                         "N": str(test_response_rates["AUD"])})
        self.assertEqual(test_response_updated["BGN"], {
                         "N": str(test_response_rates["BGN"])})
        self.assertEqual(len(test_response_updated),
                         len(test_response_rates) + 2)

    @mock.patch("main.requests.get", side_effect=mocked_requests_get)
    @mock.patch("main.reformat_json", return_value=TEST_RESPONSE_REFORMATTED)
    @mock.patch("botocore.client.BaseClient._make_api_call",
                return_value={'ResponseMetadata': {'HTTPStatusCode': 200}})
    def test_handle(self, boto_mock, mock_reformat_json, mock_get):
        response = handle(None, None)
        expected_call = [mock.call(u'PutItem', {'Item': self.test_response_reformatted,
                                                'TableName': 'exchange-rates-table'})]

        self.assertEqual(boto_mock.call_count, 1)
        boto_mock.assert_has_calls(expected_call)
        self.assertEqual(response["success"], True)
        self.assertEqual(response["status_code"], 200)
