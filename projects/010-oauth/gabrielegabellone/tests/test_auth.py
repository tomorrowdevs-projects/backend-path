import unittest
import os
from unittest.mock import patch, PropertyMock, MagicMock
from urllib.parse import urlparse, parse_qs

from oauthlib.oauth2.rfc6749.tokens import OAuth2Token
from google.oauth2.credentials import Credentials

from app import create_app
from views.auth import REDIRECT_URI, Flow, credentials_to_dict


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app(env='config.TestingConfig')
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        self.app.app_context().push()

    def test_login(self):
        """Test that the endpoint responds with status code 302 and that the location to which you are redirected is
        correct."""
        response = self.app.test_client().get('/auth/login')
        self.assertEqual(response.status_code, 302, 'Expected that the status code is 302.')

        location = response.location
        parsed_location = urlparse(location)
        query_params = parse_qs(parsed_location.query)
        actual_redirect_uri = query_params['redirect_uri'][0]
        expected_redirect_uri = REDIRECT_URI
        self.assertEqual(actual_redirect_uri, expected_redirect_uri, 'Expected another redirect URI.')

    @patch.object(Flow, 'fetch_token')
    @patch('views.auth.get_user_name')
    def test_callback(self, mock_fetch_token, mock_get_user_name):
        """Tests that the endpoint responds with status code 302 and redirects to the correct route."""
        # set a state in the session
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['state'] = 'mock_state'

        # create a fake token
        token = {'access_token': 'MTQ0NjJkZmQ5OTM2NDE1ZTZjNGZmZjI3',
                 'expires_in': 3600,
                 'scope': ['https://www.googleapis.com/auth/userinfo.profile'],
                 'token_type': 'Bearer',
                 'id_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwOi8vbXktZG9tYWluLmF1dGgwLmNvbSIsInN1YiI6ImF1dGgwfDEyMzQ1NiIsImF1ZCI6IjEyMzRhYmNkZWYiLCJleHAiOjEzMTEyODE5NzAsImlhdCI6MTMxMTI4MDk3MCwibmFtZSI6IkphbmUgRG9lIiwiZ2l2ZW5fbmFtZSI6IkphbmUiLCJmYW1pbHlfbmFtZSI6IkRvZSJ9.bql-jxlG9B_bielkqOnjTY9Di9FillFb6IMQINXoYsw',
                 'expires_at': 1690710735.4423225}
        mock_token = OAuth2Token(token)
        mock_fetch_token.return_value = mock_token

        # create fake credentials
        with patch('views.auth.Flow.credentials', new_callable=PropertyMock) as mock_flow_credentials:
            credentials = Credentials(token='MTQ0NjJkZmQ5OTM2NDE1ZTZjNGZmZjI3',
                                      token_uri='https://oauth2.googleapis.com/token',
                                      client_id='1234567890.apps.googleusercontent.com',
                                      client_secret='test_client_secret',
                                      scopes=['https://www.googleapis.com/auth/userinfo.profile'])

            mock_flow_credentials.return_value = credentials
            mock_get_user_name.return_value = 'Name Surname'

            # tests
            response = client.get('/auth/callback?state=mock_state&code=4/0AZEOvhVcZzO0')
            self.assertEqual(response.status_code, 302, 'Expected that the status code is 302.')
            self.assertEqual(response.location, '/protected_area', 'Expected to be redirected to route '
                                                                   '"/protected_area".')

    @patch('views.auth.requests')
    def test_logout(self, mock_request_check_token):
        """Tests the correct response of the endpoint in case the token check is successful."""
        # set credentials in session because this endpoint require login
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['credentials'] = {'token': '1234567890'}

        # mocked the return values for the request that checks the validity of the token
        mock_response_check_token = MagicMock()
        mock_response_check_token.status_code = 200
        mock_request_check_token.get.return_value = mock_response_check_token

        # tests
        response = client.get('/auth/logout')
        self.assertEqual(response.status_code, 200, 'Expected that the status code is 200.')
        self.assertEqual(response.json, {'message': 'Logout successful.'})

    @patch('views.auth.requests')
    def test_logout_check_token_not_ok(self, mock_request_check_token):
        """Tests the correct response of the endpoint in case the token check fails."""
        # set credentials in session because this endpoint require login
        with self.app.test_client() as client:
            with client.session_transaction() as sess:
                sess['credentials'] = {'token': '1234567890'}

        # mocked the return values for the request that checks the validity of the token
        mock_response_check_token = MagicMock()
        mock_response_check_token.ok = False

        mock_request_check_token.get.return_value = mock_response_check_token

        # tests
        response = client.get('/auth/logout')
        self.assertEqual(response.status_code, 401, 'Expected that the status code is 401.')
        self.assertEqual(response.json, {'message': 'Authorization required.'})

    def test_logout_missing_credentials(self):
        """Tests the correct response of the endpoint in case there are no credentials in the session."""
        response = self.app.test_client().get('/auth/logout')
        self.assertEqual(response.status_code, 401, 'Expected that the status code is 401.')
        self.assertEqual(response.json, {'message': 'Authorization required.'})

    def test_credentials_to_dict(self):
        """Tests the correct functioning of the `credentials_to_dict` method."""
        credentials = Credentials(token='MTQ0NjJkZmQ5OTM2NDE1ZTZjNGZmZjI3',
                                  token_uri='https://oauth2.googleapis.com/token',
                                  client_id='1234567890.apps.googleusercontent.com',
                                  client_secret='test_client_secret',
                                  scopes=['https://www.googleapis.com/auth/userinfo.profile'])
        actual = credentials_to_dict(credentials)
        expected = {'client_id': '1234567890.apps.googleusercontent.com', 'client_secret': 'test_client_secret', 'refresh_token': None, 'scopes': ['https://www.googleapis.com/auth/userinfo.profile'], 'token': 'MTQ0NjJkZmQ5OTM2NDE1ZTZjNGZmZjI3', 'token_uri': 'https://oauth2.googleapis.com/token'}
        self.assertEqual(actual, expected)
