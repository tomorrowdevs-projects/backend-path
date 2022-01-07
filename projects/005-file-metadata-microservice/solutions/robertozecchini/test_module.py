import unittest
import json
import io
from app import app, UPLOAD_PAGE, file_size
from werkzeug.datastructures import FileStorage


class UnitTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    #test if a file upload works well
    def test_upload(self):
        file_test = FileStorage(
            stream=io.BytesIO(b'abcde'),
            filename='example.pdf',
            content_type='application/pdf',
            )
        response = self.app.post(
            '/',
            data={'upload': file_test},
            content_type='multipart/form-data'
            )
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['filename'], file_test.filename)
        self.assertEqual(response_data['type'], file_test.content_type)
        self.assertEqual(response_data['size'], 5)


    #test if the server give a valid html page for upload test
    def test_html(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, UPLOAD_PAGE.encode())

if __name__ == "__main__":
    unittest.main() 