import unittest
import json
from url_shortener import app, clear_collection

class UnitTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        clear_collection()

    ###############
    #### tests ####
    ###############

    def test_post(self):
        response = self.app.post('/api/shorturl', data='http://www.example.com')
        data = json.loads(response.data)
        original_url = data['original_url']
        short_url = data['short_url']
        self.assertEqual(original_url, 'http://www.example.com')
        self.assertEqual(short_url, 1)

    def test_invalid(self):
        response = self.app.post('/api/shorturl', data='example.com')
        data = json.loads(response.data)
        error = data['error']
        self.assertEqual(error, 'invalid url')

    # external redirect not supported in test module
    # def test_redirect(self):
    #     response = self.app.post('/api/shorturl', data='http://www.example.com')
    #     data = json.loads(response.data)
    #     short_url = data['short_url']
    #     address = f'/api/shorturl/{short_url}'
    #     response = self.app.get(address, follow_redirects=True)
    #     self.assertEqual(response.status_code, 302)

    def test_wrong_redirect(self):
        address = f'/api/shorturl/1'
        response = self.app.get(address, follow_redirects=True)
        data = json.loads(response.data)
        error = data['error']
        self.assertEqual(error, 'invalid short url')

if __name__ == "__main__":
    unittest.main() 