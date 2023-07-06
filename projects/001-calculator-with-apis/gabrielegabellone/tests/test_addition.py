import unittest

from app import app


class TestAddition(unittest.TestCase):
    def setUp(self):
        self.app = app

    def test_addition(self):
        data = {"addends": [1, 2, 3.5, 4, -5]}
        response = self.app.test_client().post("/addition", json=data)
        self.assertIn(b'{"result":5.5}', response.data, "Expected result to be 5.5.")
        self.assertEqual(200, response.status_code)

    def test_addition_one_addend(self):
        data = {"addends": [20]}
        response = self.app.test_client().post("/addition", json=data)
        self.assertIn(b'{"result":20}', response.data, "Expected that if an addend is passed, the result of the "
                                                       "operation is the addend itself.")
        self.assertEqual(200, response.status_code)

    def test_addition_no_addends(self):
        data = {"addends": []}
        response = self.app.test_client().post("/addition", json=data)
        self.assertIn(b'{"result":0}', response.data, "Expected that if an empty list of addends is passed, "
                                                      "the result is 0.")
        self.assertEqual(200, response.status_code)

    def test_addition_incorrect_data_type(self):
        data = {"addends": [1, "two"]}
        response = self.app.test_client().post("/addition", json=data)
        self.assertIn(b'{"msg":"One or more invalid values. Only integers or decimals are allowed."}', response.data,
                      "Expected a different message in the response.")
        self.assertEqual(400, response.status_code)
