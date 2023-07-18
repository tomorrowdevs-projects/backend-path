import unittest
import io

from app import app


class TestAddition(unittest.TestCase):
    def setUp(self):
        self.app = app

    def test_upload_file(self):
        data = {"upfile": (io.BytesIO(b"test"), "test.txt")}
        response = self.app.test_client().post("/upload", data=data, content_type="multipart/form-data")
        self.assertIn(b'{"name":"test.txt","size":4,"type":"text/plain"}', response.data)
        self.assertEqual(200, response.status_code)
