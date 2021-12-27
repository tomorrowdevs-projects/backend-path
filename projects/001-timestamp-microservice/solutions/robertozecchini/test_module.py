import unittest
import json
import time
import datetime
import urllib.parse
from app import app
from dateutil.parser import parse

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
    
    #test if the server give a valid answer on main page
    def test_main_page(self):
        response = self.app.get('/api/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    #test if the conversion from string to unix timestamps works
    def test_date_2_unix(self):
        address = '/api/:Sat, 01 Jan 2022 00:00:00 GMT?'
        address = urllib.parse.quote(address)
        response = self.app.get(address, follow_redirects=True)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['unix'], 1640995200000)
    
    # test if a not UTC date is read in a proper way
    def test_date_not_utc(self):
        address = '/api/:Sat, 01 Jan 2022 00:00:00 CET?'
        address = urllib.parse.quote(address)
        response = self.app.get(address, follow_redirects=True)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['unix'], 1640991600000)
    
    # test if a not UTC date is converted in a proper way
    def test_date_2_utc(self):
        address = '/api/:Sat, 01 Jan 2022 00:00:00 CET?'
        address = urllib.parse.quote(address)
        response = self.app.get(address, follow_redirects=True)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['utc'], "Fri, 31 Dec 2021 23:00:00 GMT")
    
    # test if an invalid date produce the right error
    def test_invalid_date(self):
        address = '/api/:00 Jan 0000 00:00:00 GMT?'
        address = urllib.parse.quote(address)
        response = self.app.get(address, follow_redirects=True)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['error'], "Invalid Date")
    
    # test if an invalid input produce the right error
    def test_invalid_input(self):
        address = '/api/Pippo'
        response = self.app.get(address, follow_redirects=True)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['error'], "Invalid Date")
    
    # test if a numeric unix timestamp produces a right date
    def test_numeric_input(self):
        address = '/api/1451001600000'
        response = self.app.get(address, follow_redirects=True)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['unix'], 1451001600000)
        self.assertEqual(response_data['utc'], "Fri, 25 Dec 2015 00:00:00 GMT")
    
    # test if unix timestamp of actual time is ok (1 second error permitted)
    def test_now_unix(self):
        address = '/api/'
        response = self.app.get(address, follow_redirects=True)
        response_data = json.loads(response.data)
        now = time.time()
        now_read = response_data['unix']
        delta = abs(now - now_read)
        self.assertLessEqual(delta, 1)
    
    # test if utc timestamp of actual time is ok (1 second error permitted)
    def test_now_unix(self):
        address = '/api/'
        response = self.app.get(address, follow_redirects=True)
        response_data = json.loads(response.data)
        now = time.time()
        now_read = parse(response_data['utc'])
        now_read = datetime.datetime.timestamp(now_read)
        delta = abs(now - now_read)
        self.assertLessEqual(delta, 1)

if __name__ == "__main__":
    unittest.main()