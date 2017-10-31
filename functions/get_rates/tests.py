from unittest import TestCase
import boto3
from botocore.stub import Stubber

from main import reformat_json


class TestClass(TestCase):

    def setUp(self):
        self.test_response = {
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

    def test_reformat_json(self):
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

    def test_handle(self):
        pass
