import datetime

from flask import Blueprint, request, make_response, jsonify, current_app
from flasgger import swag_from
import jwt


bp = Blueprint("auth", __name__)

user = {"email": "test@email.com", "password": "test"}

access_token_lifetime = 30
refresh_token_lifetime = 50
blacklist_tokens = []


def token_required(function):
    def wrapper():
        headers = request.headers

        if "Authorization" in headers:
            token = headers["Authorization"][7:]
        elif "x-access-token" in headers:
            token = headers["x-access-token"]
        else:
            return make_response(jsonify({"msg": "Authorization required."}), 401)

        key = current_app.config["SECRET_KEY"]

        try:
            data = jwt.decode(token, key, algorithms="HS256")
            if data["email"] == user["email"]:
                return function()
        except jwt.exceptions.ExpiredSignatureError:
            return make_response(jsonify({"msg": "Token is expired."}), 400)
        except jwt.exceptions.DecodeError:
            return make_response(jsonify({"msg": "Error decoding token."}), 400)

    wrapper.__name__ = function.__name__
    return wrapper


def generate_token(duration: int, payload: dict) -> str:
    """Takes care of generating a token.

    :param duration: indicates the duration of the token in seconds
    :param payload: dict that contains the claims
    :raises KeyError: if the payload does not contain the key "exp"
    :return: the JWT
    """
    key = current_app.config["SECRET_KEY"]
    payload["exp"] += datetime.timedelta(seconds=duration)
    token = jwt.encode(payload, key, algorithm="HS256")
    return token


@bp.route("/login", methods=["POST"])
@swag_from("../docs/login.yml")
def login():
    data = request.get_json()
    try:
        email = data["email"]
        password = data["password"]

        if user["email"] == email and user["password"] == password:
            payload = {"iat": datetime.datetime.utcnow(), "exp": datetime.datetime.utcnow(), "email": email}
            access_token = generate_token(access_token_lifetime, payload)
            refresh_token = generate_token(refresh_token_lifetime, payload)
            return make_response(jsonify({"token": access_token, "refresh_token": refresh_token}), 200)
        return make_response(jsonify({"msg": "Bad username or password"}), 401)

    except KeyError:
        return make_response(jsonify({"msg": "Bad request"}), 400)


@bp.route("/refresh", methods=["POST"])
@swag_from("../docs/refresh.yml")
def refresh():
    data = request.get_json()
    key = current_app.config["SECRET_KEY"]
    try:
        refresh_token = data["refresh_token"]
        decoded = jwt.decode(refresh_token, key, algorithms="HS256")
        payload = {"iat": datetime.datetime.utcnow(), "exp": datetime.datetime.utcnow(), "email": decoded["email"]}
        return make_response(jsonify({"token": generate_token(refresh_token_lifetime, payload),
                                      "refresh_token": generate_token(refresh_token_lifetime, payload)}), 200)

    except KeyError:
        return make_response(jsonify({"msg": "Refresh token is missing."}), 400)
    except jwt.exceptions.ExpiredSignatureError:
        return make_response(jsonify({"msg": "Token is expired."}), 400)
    except jwt.exceptions.DecodeError:
        return make_response(jsonify({"msg": "Error decoding token."}), 400)


@bp.route("/logout", methods=["POST"])
@swag_from("../docs/logout.yml")
@token_required
def logout():
    token = request.headers["Authorization"][7:]
    blacklist_tokens.append(token)
    return make_response(jsonify({'msg': 'Logout success'}), 200)
