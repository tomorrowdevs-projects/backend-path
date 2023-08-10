import unittest
from unittest.mock import patch, MagicMock
import os

from app import create_app


class TestIndex(unittest.TestCase):
    def setUp(self):
        self.app = create_app(env='config.TestingConfig')
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        self.app.app_context().push()

    @patch('views.auth.requests')
    def test_protected_area(self, mock_requests):
        """Test the correct response of the endpoint after user authentication."""
        # set credentials in session because this endpoint require login
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['credentials'] = {'token': '1234567890'}
                sess['name'] = 'Name Surname'

        # mocked the return values for the request that checks the validity of the token
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_requests.get.return_value = mock_response

        # tests
        response = client.get('/protected_area')
        self.assertEqual(response.status_code, 200, 'Expected that the status code is 200.')
        self.assertEqual(response.text, 'Welcome to the protected area, Name Surname <a '
                                        'href="/auth/logout"?><button>Logout</button></a>')
