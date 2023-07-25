import unittest

from app import create_test_app
from tests.populate_db import populate_db
from models import db


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_test_app()
        db.create_all()
        populate_db(db)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        """Test of the case where the login was successful."""
        data = {"username": "mariorossi", "password": "password"}
        response = self.app.test_client().post('/auth/login', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"message":"Login successful"}', response.data)

    def test_login_user_not_found(self):
        """Testing the case where login failed, because the user is not found."""
        data = {"username": "marioross", "password": "password"}
        response = self.app.test_client().post('/auth/login', json=data)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'{"message":"User not found. Username or Password Error"}', response.data)

    def test_logout(self):
        """Testing the case where logout was successful."""
        # login
        data = {"username": "mariorossi", "password": "password"}
        self.app.test_client().post('/auth/login', json=data)

        # logout
        response = self.app.test_client().post('/auth/logout')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'{"message":"Logout successful"}', response.data)

    def test_logout_not_successful(self):
        """Test of the case in which you are logged out without logging in first."""
        response = self.app.test_client().post('/auth/logout')
        # the decorator @login_required redirects to the login page if the user is not logged in, for this it returns
        # status code 302
        self.assertEqual(response.status_code, 302)
