import unittest
import datetime
import jwt

from jwt_auth.token import generate_token, extract_token

class TestToken(unittest.TestCase):
    def test_generate_token(self):
        payload = {"iat": datetime.datetime.utcnow(), "exp": datetime.datetime.utcnow(), "username": "test"}
        duration = 5
        key = "key"
        token = generate_token(duration, payload, key)
        decoded_token = jwt.decode(token, "key", algorithms="HS256")
        self.assertEqual(decoded_token["username"], "test")
    
    def test_generate_token_no_exp(self):
        payload = {"iat": datetime.datetime.utcnow(), "username": "test"}
        duration = 5
        key = "key"
        with self.assertRaises(KeyError):
            generate_token(duration, payload, key)
    
    def test_extract_token(self):
        data = {"x-access-token": "token"}
        actual = extract_token(data)
        expected = "token"
        self.assertEqual(actual, expected)
        data = {"Authorization": "Bearer token"}
        expected = "token"
        self.assertEqual(actual, expected)

    def test_extract_token_error(self):
        data = {"token": "token"}
        with self.assertRaises(Exception):
            extract_token(data)
            