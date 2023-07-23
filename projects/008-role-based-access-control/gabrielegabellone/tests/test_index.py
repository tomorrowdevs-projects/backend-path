import unittest

from flask_login import FlaskLoginClient

from app import create_test_app
from tests.populate_db import populate_db
from models import db, User


class TestIndex(unittest.TestCase):
    def setUp(self):
        self.app = create_test_app()
        self.app.test_client_class = FlaskLoginClient
        db.create_all()
        populate_db(db)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_regular_area_admin_user(self):
        """Test where you try to log in with an admin user in an area where all user types can log in."""
        user_id = 1
        user = db.session.get(User, user_id)
        with self.app.test_client(user=user) as client:
            response = client.get("/regular-area")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'Welcome to the regular area, mariorossi.')

    def test_regular_area_regular_user(self):
        """Test where you try to log in with a non-admin user in an area where all user types can log in."""
        user_id = 2
        user = db.session.get(User, user_id)
        with self.app.test_client(user=user) as client:
            response = client.get("/regular-area")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'Welcome to the regular area, lucaverdi.')

    def test_admin_area_admin_user(self):
        """Test where you try to log in with an admin user in an area where only admin users can log in."""
        user_id = 1
        user = db.session.get(User, user_id)
        with self.app.test_client(user=user) as client:
            response = client.get("/admin-area")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'Welcome to the admin area, mariorossi.')

    def test_admin_area_regular_user(self):
        """Test where you try to log in with a non-admin user in an area where only admin users can log in."""
        user_id = 2
        user = db.session.get(User, user_id)
        with self.app.test_client(user=user) as client:
            response = client.get("/admin-area")
            self.assertEqual(response.status_code, 403)
            self.assertIn(b'{"message":"Reserved area for admin users."}', response.data)
