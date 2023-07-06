import unittest

from app import app


class TestSubtraction(unittest.TestCase):
    def setUp(self):
        self.app = app

    def test_subtraction(self):
        data = {"minuend": 10, "subtrahends": [3, 5.5, -6]}
        response = self.app.test_client().post("/subtraction", json=data)
        self.assertIn(b'{"result":7.5}', response.data, "Expected result to be 7.5.")
        self.assertEqual(200, response.status_code)

    def test_subtraction_no_subtrahends(self):
        data = {"minuend": 10, "subtrahends": []}
        response = self.app.test_client().post("/subtraction", json=data)
        self.assertIn(b'{"result":10}', response.data, "Expected that if an empty list of subtrahends is passed, "
                                                      "the result is the minuend itself.")
        self.assertEqual(200, response.status_code)

    def test_subtraction_incorrect_data_type(self):
        data = {"minuend": 10, "subtrahends": [1, "two"]}
        response = self.app.test_client().post("/subtraction", json=data)
        self.assertIn(b'{"msg":"One or more invalid values. Only integers or decimals are allowed."}', response.data,
                      "Expected a different message in the response.")
        self.assertEqual(400, response.status_code)
