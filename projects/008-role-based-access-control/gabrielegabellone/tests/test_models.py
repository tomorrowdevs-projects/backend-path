import unittest

from models import User, Role


class TestRole(unittest.TestCase):
    def setUp(self):
        self.role1 = Role(id=1, name="admin")
        self.role2 = Role(id=2, name="regular user")

    def test_repr(self):
        """Test of the correct string representation of the Role model."""
        actual = str(self.role1)
        expected = "<id: 1, name: admin>"
        self.assertEqual(actual, expected, "Expected a different string representation.")
        actual = str(self.role2)
        expected = "<id: 2, name: regular user>"
        self.assertEqual(actual, expected, "Expected a different string representation.")


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user1 = User(id=1, username="mariorossi", password="password")
        self.user1.role = Role(id=1, name="admin")
        self.user2 = User(id=2, username="lucaverdi", password="password")
        self.user2.role = Role(id=2, name="regular user")

    def test_repr(self):
        """Test of the correct string representation of the User model."""
        actual = str(self.user1)
        expected = "<id: 1, username: mariorossi, role: admin>"
        self.assertEqual(actual, expected, "Expected a different string representation.")
        actual = str(self.user2)
        expected = "<id: 2, username: lucaverdi, role: regular user>"
        self.assertEqual(actual, expected, "Expected a different string representation.")
