import unittest

from app import app


class TestMultiplication(unittest.TestCase):
    def setUp(self):
        self.app = app

    def test_multiplication(self):
        data = {"multiplicand": 5, "multiplicators": [2, 0.5, -2]}
        response = self.app.test_client().post("/multiplication", json=data)
        self.assertIn(b'{"result":-10.0}', response.data, "Expected result to be -10.0.")
        self.assertEqual(200, response.status_code)

    def test_multiplication_no_multiplicators(self):
        data = {"multiplicand": 5, "multiplicators": []}
        response = self.app.test_client().post("/multiplication", json=data)
        self.assertIn(b'{"result":5}', response.data, "Expected that if an empty list of multiplicators is passed, "
                                                      "the result is the multiplicand itself.")
        self.assertEqual(200, response.status_code)

    def test_multiplication_incorrect_data_type(self):
        data = {"multiplicand": 5, "multiplicators": [1, "two"]}
        response = self.app.test_client().post("/multiplication", json=data)
        self.assertIn(b'{"msg":"One or more invalid values. Only integers or decimals are allowed."}', response.data,
                      "Expected a different message in the response.")
        self.assertEqual(400, response.status_code)
