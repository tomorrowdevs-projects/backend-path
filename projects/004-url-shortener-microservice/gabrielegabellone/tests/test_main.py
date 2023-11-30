import unittest

from fastapi.testclient import TestClient

from main import app


class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_short_url(self):
        original_url = "https://www.google.it/"
        response = self.client.post("/api/shorturl", json={"original_url": original_url})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"original_url": original_url, "short_url": 1})

    def test_create_short_url_invalid_url(self):
        original_url = "https//www.google.it/"
        response = self.client.post("/api/shorturl", json={"original_url": original_url})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "invalid url"})

    def test_redirect_to_original_url(self):
        original_url = "https://tomorrowdevs.com"
        response = self.client.post("/api/shorturl", json={"original_url": original_url})

        # without the follow_redirects parameter the test returns status code 404
        short_url = response.json()["short_url"]
        response = self.client.get(f"/api/shorturl/{short_url}", follow_redirects=False)
        self.assertEqual(response.status_code, 307)

    def test_redirect_to_original_url_short_url_not_found(self):
        short_url = 3
        response = self.client.get(f"/api/shorturl/{short_url}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "short url not found"})
