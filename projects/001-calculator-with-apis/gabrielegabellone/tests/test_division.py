import unittest

from app import app


class TestDivision(unittest.TestCase):
    def setUp(self):
        self.app = app

    def test_division(self):
        data = {"dividend": 50, "divisors": [0.5, 4, -5]}
        response = self.app.test_client().post("/division", json=data)
        self.assertIn(b'{"result":-5.0}', response.data, "Expected result to be -5.0.")
        self.assertEqual(200, response.status_code)

    def test_division_no_divisors(self):
        data = {"dividend": 50, "divisors": []}
        response = self.app.test_client().post("/division", json=data)
        self.assertIn(b'{"result":50}', response.data, "Expected that if an empty list of divisors is passed, "
                                                      "the result is the dividend itself.")
        self.assertEqual(200, response.status_code)

    def test_division_incorrect_data_type(self):
        data = {"dividend": 50, "divisors": [1, "two"]}
        response = self.app.test_client().post("/division", json=data)
        self.assertIn(b'{"msg":"One or more invalid values. Only integers or decimals are allowed."}', response.data,
                      "Expected a different message in the response.")
        self.assertEqual(400, response.status_code)

    def test_division_divide_by_0(self):
        data = {"dividend": 50, "divisors": [5, 0]}
        response = self.app.test_client().post("/division", json=data)
        self.assertIn(b'{"msg":"You cannot divide a number by 0."}', response.data,
                      "Expected a different message in the response.")
        self.assertEqual(400, response.status_code)
