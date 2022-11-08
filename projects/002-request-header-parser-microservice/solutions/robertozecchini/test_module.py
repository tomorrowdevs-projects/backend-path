import unittest
import json
from whoami import app

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

    def test_status_code(self):
        response = self.app.get('/api/whoami', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_ip(self):
        response = self.app.get('/api/whoami', follow_redirects=True)
        data = json.loads(response.data)
        ip = data['ip']
        self.assertEqual(ip, '127.0.0.1')

    def test_language_na(self):
        response = self.app.get('/api/whoami', follow_redirects=True)
        data = json.loads(response.data)
        language = data['language']
        self.assertEqual(language, 'n.a.')
    
    def test_language(self):
        response = self.app.get('/api/whoami', follow_redirects=True, headers = {'Accept-Language': 'it'})
        data = json.loads(response.data)
        language = data['language']
        self.assertEqual(language, 'it')

    def test_software(self):
        response = self.app.get('/api/whoami', follow_redirects=True, headers = {'User-Agent': 'test_software'})
        data = json.loads(response.data)
        software = data['software']
        self.assertEqual(software, 'test_software')

if __name__ == "__main__":
    unittest.main() 