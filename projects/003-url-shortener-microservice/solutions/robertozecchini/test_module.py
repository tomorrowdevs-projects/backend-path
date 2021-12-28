import unittest
import json
from url_shortener import app

class UnitTests(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    # def test_status_code(self):
    #     response = self.app.get('/api/shorturl', follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.app.post('/api/shorturl', data='http://www.example.com')
        data = json.loads(response.data)
        original_url = data['original_url']
        short_url = data['short_url']
        self.assertEqual(original_url, 'http://www.example.com')
        self.assertEqual(short_url, 1)


if __name__ == "__main__":
    unittest.main() 