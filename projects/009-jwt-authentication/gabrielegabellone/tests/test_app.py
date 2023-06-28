import unittest
from unittest.mock import patch
import jwt
import datetime

from app import app, generate_token
import app as main

main.user = {"email": "gabriele@email.com", "password": "secretpassword", "username": "Gabriele"}


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.app_context().push()

    def test_login(self):
        user = {"email": "gabriele@email.com", "password": "secretpassword"}
        response = self.app.test_client().post('/login', json=user)
        data = response.get_json()
        self.assertIn("token", data, "Expected that the response contains an access token.")
        self.assertIn("refresh_token", data, "Expected that the response contains a refresh token.")
        self.assertEqual(200, response.status_code)

    def test_login_incorrect_email(self):
        user = {"email": "gabriele@email.co", "password": "secretpassword"}
        response = self.app.test_client().post('/login', json=user)
        self.assertIn(b'{"msg":"Bad username or password"}', response.data)
        self.assertEqual(401, response.status_code)        

    def test_login_incorrect_password(self):
        user = {"email": "gabriele@email.com", "password": "secretpasswor"}
        response = self.app.test_client().post('/login', json=user)
        self.assertIn(b'{"msg":"Bad username or password"}', response.data)
        self.assertEqual(401, response.status_code)

    def test_login_incomplete_data(self):
        user = {"email": "gabriele@email.com"}
        response = self.app.test_client().post('/login', json=user)
        self.assertIn(b'{"msg":"Bad request"}', response.data)
        self.assertEqual(400, response.status_code)

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.app_context().push()
        user = {"email": "gabriele@email.com", "password": "secretpassword"}
        response = self.app.test_client().post('/login', json=user)
        data = response.get_json()
        self.access_token = data["token"]
        self.refresh_token = data["refresh_token"]    
    
    def test_homepage(self):
        response = self.app.test_client().get('/')
        self.assertIn(b"This is an unprotected route.", response.data)

    def test_homepage_user(self):
        response = self.app.test_client().get('/user', headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertIn(b"Welcome Gabriele!", response.data)

    def test_homepage_user_missing_token(self):
        data = {}
        response = self.app.test_client().get('/user', json=data)
        self.assertIn(b'{"msg":"Authorization required."}', response.data)
        self.assertEqual(401, response.status_code)

    @patch('app.jwt.decode')    
    def test_homepage_user_expired_token(self, mock):
        mock.side_effect = jwt.exceptions.ExpiredSignatureError
        response = self.app.test_client().get('/user', headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertIn(b'{"msg":"Token is expired."}', response.data)
        self.assertEqual(400, response.status_code)

    def test_homepage_user_token_not_valid(self):
        response = self.app.test_client().get('/user', headers={"Authorization": f"Bearer token"})
        self.assertIn(b'{"msg":"Error decoding token."}', response.data)
        self.assertEqual(400, response.status_code)
    
    def test_refresh(self):
        data = {"refresh_token": self.refresh_token}
        response = self.app.test_client().post('/refresh', json=data)
        access_token = response.get_json()["token"]
        response = self.app.test_client().get('/user', headers={"Authorization": f"Bearer {access_token}"})
        self.assertIn(b"Welcome Gabriele!", response.data)

    def test_refresh_missing_token(self):
        data = {}
        response = self.app.test_client().post('/refresh', json=data)
        self.assertIn(b'{"msg":"Refresh token is missing."}', response.data)
        self.assertEqual(400, response.status_code)

    @patch('app.jwt.decode')
    def test_refresh_expired_token(self, mock):
        mock.side_effect = jwt.exceptions.ExpiredSignatureError
        data = {"refresh_token": self.refresh_token}
        response = self.app.test_client().post('/refresh', json=data)
        self.assertIn(b'{"msg":"Token is expired."}', response.data)
        self.assertEqual(400, response.status_code)

    def test_refresh_token_not_valid(self):
        data = {"refresh_token": "refresh token"}
        response = self.app.test_client().post('/refresh', json=data)
        self.assertIn(b'{"msg":"Error decoding token."}', response.data)
        self.assertEqual(400, response.status_code)


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