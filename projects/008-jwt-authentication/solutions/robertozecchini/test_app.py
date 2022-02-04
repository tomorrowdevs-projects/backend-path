import unittest
import time

from app import app, access_duration

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_00_home_unauthenticated(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.get_json())
        self.assertEqual(response.get_json()["error"], "Missing token")

    def test_01_login_wrong(self):
        response = self.client.post("/login", json = {"username":"foo","password":"bar"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.get_json())
        self.assertEqual(response.get_json()["error"], "Invalid username or password")

    def test_02_login_right(self):
        response = self.client.post("/login", json = {"username":"user1","password":"password1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.get_json())
        self.assertIn("refresh_token", response.get_json())

    def test_03_auth_right(self):
        response = self.client.post("/login", json = {"username":"user1","password":"password1"})
        access_token = response.get_json()["access_token"]
        response = self.client.get("/", headers = {"authorization": "Bearer "+access_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello", response.get_json())
        self.assertEqual(response.get_json()["Hello"], "user1")

    def test_04_auth_wrong_type(self):
        response = self.client.post("/login", json = {"username":"user1","password":"password1"})
        refresh_token = response.get_json()["refresh_token"]
        response = self.client.get("/", headers = {"authorization": "Bearer "+refresh_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.get_json())
        self.assertEqual(response.get_json()["error"], "Invalid token type")

    def test_05_auth_wrong(self):
        response = self.client.get("/", headers = {"authorization": "Bearer xxx"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.get_json())
        self.assertEqual(response.get_json()["error"], "Invalid token")

    def test_06_token_expired(self):
        response = self.client.post("/login", json = {"username":"user1","password":"password1"})
        access_token = response.get_json()["access_token"]
        time.sleep(access_duration+1)
        response = self.client.get("/", headers = {"authorization": "Bearer "+access_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.get_json())
        self.assertEqual(response.get_json()["error"], "Signature expired")
    
    def test_07_refresh(self):
        response = self.client.post("/login", json = {"username":"user1","password":"password1"})
        access_token = response.get_json()["access_token"]
        refresh_token = response.get_json()["refresh_token"]
        time.sleep(access_duration+1)
        response = self.client.get("/", headers = {"authorization": "Bearer "+access_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("error", response.get_json())
        self.assertEqual(response.get_json()["error"], "Signature expired")
        response = self.client.get("/refresh", headers = {"authorization": "Bearer "+refresh_token})
        access_token = response.get_json()["access_token"]
        refresh_token = response.get_json()["refresh_token"]
        response = self.client.get("/", headers = {"authorization": "Bearer "+access_token})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello", response.get_json())
        self.assertEqual(response.get_json()["Hello"], "user1")
        


if __name__ == "__main__":
    unittest.main()