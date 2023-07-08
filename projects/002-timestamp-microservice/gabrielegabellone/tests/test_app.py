import unittest
import datetime
import json

from app import app
from microservices import date_service


class TestDateService(unittest.TestCase):
    def setUp(self):
        self.app = app

    def test_from_datetime_to_utc(self):
        date_to_convert = datetime.date(year=2023, month=7, day=8)
        actual = date_service.from_datetime_to_utc(date_to_convert)
        expected = "Sat, 08 Jul 2023 00:00:00 GMT"
        self.assertEqual(expected, actual)

    def test_from_date_to_unix_and_utc(self):
        response = self.app.test_client().get("/api/:date?year=2023&month=7&day=7")
        self.assertIn(b'{"unix":1688680800.0,"utc":"Fri, 07 Jul 2023 00:00:00 GMT"}', response.data,
                      "Expected the result to be the unix timestamp and UTC of 2023/7/7.")
        self.assertEqual(200, response.status_code)

    def test_from_date_to_unix_and_utc_no_query_parameters(self):
        expected_date = datetime.date.today()
        response = self.app.test_client().get("/api/:date")
        decoded_response = json.loads(response.data.decode('utf-8'))
        returned_date = datetime.datetime.fromtimestamp(decoded_response["unix"])

        self.assertEqual(expected_date.day, returned_date.day, "Expected that in the absence of the 'day' parameter, "
                                                               "the current day is passed by default.")
        self.assertEqual(expected_date.month, returned_date.month, "Expected that in the absence of the 'month' "
                                                                   "parameter, the current month is passed by default.")
        self.assertEqual(expected_date.year, returned_date.year, "Expected that in the absence of the 'year' "
                                                                 "parameter, the current year is passed by default.")
        self.assertEqual(200, response.status_code)

    def test_from_date_to_unix_and_utc_value_error(self):
        response = self.app.test_client().get("/api/:date?year=2023&month=17&day=7")
        self.assertIn(b'{"error":"Invalid Date"}', response.data, "Expected a different error message.")
        self.assertEqual(200, response.status_code)

    def test_from_unix_to_utc(self):
        response = self.app.test_client().get("/api/1450998000")
        self.assertIn(b'{"unix":1450998000,"utc":"Thu, 24 Dec 2015 23:00:00 GMT"}', response.data,
                      "Expected the result to be the unix timestamp and UTC of 2015/12/25.")
        self.assertEqual(200, response.status_code)

    def test_from_unix_to_utc_unix_not_valid(self):
        not_valid_unix_timestamp = 1451001600001
        response = self.app.test_client().get(f"/api/{not_valid_unix_timestamp}")
        self.assertIn(b'{"error":"unix timestamp not valid"}', response.data, "Expected a different error message.")
        self.assertEqual(400, response.status_code)
        