import unittest
from unittest.mock import patch
import jwt

from app import app


class TestIndex(unittest.TestCase):
    def setUp(self):
        self.app = app
        app.app_context().push()
        user = {"email": "test@email.com", "password": "test"}
        response = self.app.test_client().post("/auth/login", json=user)

        data = response.get_json()
        self.access_token = data["token"]
        self.refresh_token = data["refresh_token"]

    def test_homepage(self):
        """Test the response of the endpoint by accessing it without providing an authentication token."""
        response = self.app.test_client().get("/")
        self.assertIn(b"This is the homepage and it is an unprotected route.", response.data)

    def test_protected_area(self):
        """Test the response of the endpoint by accessing it with authentication."""
        response = self.app.test_client().get("/protected-area",
                                              headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertIn(b"Welcome in the protected area", response.data)

    def test_protected_area_missing_token(self):
        """Test the response of the endpoint by accessing it without providing an authentication token."""
        response = self.app.test_client().get("/protected-area")
        self.assertIn(b'{"msg":"Authorization required."}', response.data)
        self.assertEqual(401, response.status_code)

    @patch('views.auth.jwt.decode')
    def test_protected_area_expired_token(self, mock):
        """Test the response of the endpoint by accessing it with an expired token."""
        mock.side_effect = jwt.exceptions.ExpiredSignatureError
        response = self.app.test_client().get("protected-area",
                                              headers={"Authorization": f"Bearer {self.access_token}"})
        self.assertIn(b'{"msg":"Token is expired."}', response.data)
        self.assertEqual(400, response.status_code)

    def test_protected_area_token_not_valid(self):
        """Test the response of the endpoint by accessing it with an invalid token."""
        response = self.app.test_client().get("/protected-area", headers={"Authorization": f"Bearer token"})
        self.assertIn(b'{"msg":"Error decoding token."}', response.data)
        self.assertEqual(400, response.status_code)
