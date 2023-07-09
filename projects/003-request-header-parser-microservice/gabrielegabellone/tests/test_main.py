import unittest

from fastapi.testclient import TestClient

from main import app


class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_who_am_i(self):
        response = self.client.get("/api/whoami", headers={"language": "Python", "software": "Pycharm"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ipaddress": "testclient", "language": "Python", "software": "Pycharm"})

    def test_who_am_i_no_header(self):
        response = self.client.get("/api/whoami")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ipaddress": "testclient", "language": None, "software": None})
