import unittest
from unittest.mock import patch
import datetime

import jwt

from app import app
from views.auth import generate_token


class TestToken(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.app_context().push()

    def test_generate_token(self):
        """Test that the token is generated correctly."""
        payload = {"iat": datetime.datetime.utcnow(), "exp": datetime.datetime.utcnow(), "username": "test"}
        duration = 5

        token = generate_token(duration, payload)
        decoded_token = jwt.decode(token, "your secret key", algorithms="HS256")
        self.assertEqual(decoded_token["username"], "test")

    def test_generate_token_no_exp(self):
        """Tests for a KeyError to be raised if a payload is provided without the 'exp' key."""
        payload = {"iat": datetime.datetime.utcnow(), "username": "test"}
        duration = 5

        with self.assertRaises(KeyError):
            generate_token(duration, payload)


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.user = {"email": "test@email.com", "password": "test"}
        app.app_context().push()

    def test_login(self):
        """Test the response of the endpoint if correct email and password are provided."""
        response = self.app.test_client().post('/auth/login', json=self.user)
        data = response.get_json()
        self.assertIn("token", data, "Expected that the response contains an access token.")
        self.assertIn("refresh_token", data, "Expected that the response contains a refresh token.")
        self.assertEqual(200, response.status_code)

    def test_login_incorrect_email(self):
        """Test the response of the endpoint if the incorrect email is provided."""
        user = {"email": "test@email.co", "password": "test"}
        response = self.app.test_client().post('/auth/login', json=user)
        self.assertIn(b'{"msg":"Bad username or password"}', response.data)
        self.assertEqual(401, response.status_code)

    def test_login_incorrect_password(self):
        """Test the response of the endpoint if the incorrect password is provided."""
        user = {"email": "test@email.com", "password": "testt"}
        response = self.app.test_client().post('/auth/login', json=user)
        self.assertIn(b'{"msg":"Bad username or password"}', response.data)
        self.assertEqual(401, response.status_code)

    def test_login_incomplete_data(self):
        """Test the response of the endpoint if incomplete data is provided, for example if the password is missing."""
        user = {"email": "test@email.com"}
        response = self.app.test_client().post('/auth/login', json=user)
        self.assertIn(b'{"msg":"Bad request"}', response.data)
        self.assertEqual(400, response.status_code)


class TestRefreshLogout(unittest.TestCase):
    """Test cases that go to test endpoints that require authentication tokens, for this a login is made in the setup"""
    def setUp(self):
        self.app = app
        app.app_context().push()
        user = {"email": "test@email.com", "password": "test"}
        response = self.app.test_client().post('/auth/login', json=user)

        data = response.get_json()
        self.access_token = data["token"]
        self.refresh_token = data["refresh_token"]

    def test_refresh(self):
        """Test that the endpoint that refreshes the token is working correctly by trying to access the protected
        area with the refreshed token."""
        data = {"refresh_token": self.refresh_token}
        response = self.app.test_client().post('/auth/refresh', json=data)
        access_token = response.get_json()["token"]
        response = self.app.test_client().get('/protected-area', headers={"Authorization": f"Bearer {access_token}"})
        self.assertIn(b"Welcome in the protected area", response.data)

    def test_refresh_missing_token(self):
        """Test the response of the endpoint when trying to refresh the tokens without providing the refresh token."""
        data = {}
        response = self.app.test_client().post('/auth/refresh', json=data)
        self.assertIn(b'{"msg":"Refresh token is missing."}', response.data)
        self.assertEqual(400, response.status_code)

    @patch('views.auth.jwt.decode')
    def test_refresh_expired_token(self, mock):
        """Test the response of the endpoint when trying to refresh tokens by providing an expired refresh token."""
        mock.side_effect = jwt.exceptions.ExpiredSignatureError
        data = {"refresh_token": self.refresh_token}
        response = self.app.test_client().post('/auth/refresh', json=data)
        self.assertIn(b'{"msg":"Token is expired."}', response.data)
        self.assertEqual(400, response.status_code)

    def test_refresh_token_not_valid(self):
        """Test the response of the endpoint when trying to refresh tokens by providing an invalid refresh token."""
        data = {"refresh_token": "refresh token"}
        response = self.app.test_client().post('/auth/refresh', json=data)
        self.assertIn(b'{"msg":"Error decoding token."}', response.data)
        self.assertEqual(400, response.status_code)

    def test_logout(self):
        """Test the response of the logout endpoint when the token is provided."""
        response = self.app.test_client().post('/auth/logout', headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertIn(b'{"msg":"Logout success"}', response.data)
        self.assertEqual(200, response.status_code)
