import requests
from flask import Blueprint, session, redirect, request, current_app, make_response, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

bp = Blueprint("auth", __name__)

SCOPES = ['https://www.googleapis.com/auth/userinfo.profile']
REDIRECT_URI = 'http://127.0.0.1:5000/auth/callback'


def credentials_to_dict(credentials: Credentials) -> dict:
    """Takes care of converting an object of type Credentials to dict.

    :param credentials: the object to convert
    :return: the object converted to dict
    """
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


def get_user_name(token: str) -> str:
    """Takes care of getting the full name of the user.

    :param token: the token to perform the request
    :return: the full name of the user
    """
    get_user = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
                            headers={'Authorization': f'Bearer {token}'})
    name = get_user.json()['name']
    return name


def login_required(function):
    """Protects the route of the view function passed as a parameter. Check if there is a token in the session and if
    yes, check its validity.

    :param function: the view function of the route to be protected
    :return: the function passed as a parameter, otherwise it responds with status code 401 if the check is not successful
    """
    def wrapper(*args, **kwargs):
        if 'credentials' in session:
            credentials = session['credentials']
            if 'token' in credentials:
                token = credentials['token']
                check_token = requests.get(f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}')
                if check_token.ok:
                    return function()
        return make_response(jsonify({'message': 'Authorization required.'}), 401)
    return wrapper


@bp.route('/login')
def login():
    client_secrets_file = current_app.config['CLIENT_SECRET_JSON_PATH']

    flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file, scopes=SCOPES)
    flow.redirect_uri = REDIRECT_URI

    authorization_url, state = flow.authorization_url(include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state

    return redirect(authorization_url)


@bp.route('/callback')
def callback():
    # Specify the state when creating the flow in the callback so that it can be verified in the authorization server
    # response.
    state = session['state']
    client_secrets_file = current_app.config['CLIENT_SECRET_JSON_PATH']

    flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file, scopes=SCOPES, state=state)
    flow.redirect_uri = REDIRECT_URI

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials and user name in the session.
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    session['name'] = get_user_name(credentials.token)

    return redirect('/protected_area')


@bp.route('/logout')
@login_required
def logout():
    credentials = Credentials(**session['credentials'])

    requests.post('https://oauth2.googleapis.com/revoke',
                  params={'token': credentials.token},
                  headers={'content-type': 'application/x-www-form-urlencoded'})

    session.clear()
    return {'message': 'Logout successful.'}
