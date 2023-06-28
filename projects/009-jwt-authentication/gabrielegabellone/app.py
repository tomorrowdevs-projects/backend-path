import datetime
import jwt

from flask import Flask, request, jsonify, make_response


app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"

user = {"email": "test@email.com", "password": "test", "username": "test"}
access_token_lifetime = 30
refresh_token_lifetime = 50
key = app.config["SECRET_KEY"]

def token_required(function):
    def wrapper():
        headers = request.headers

        if "Authorization" in headers:
            token = headers["Authorization"][7:]
        elif "x-access-token" in headers:
            token = headers["x-access-token"]
        else:
            return make_response(jsonify({"msg" : "Authorization required."}), 401)

        try:
            data = jwt.decode(token, key, algorithms="HS256")
            if data["email"] == user["email"]:
                return function(user)
        except jwt.exceptions.ExpiredSignatureError:
            return make_response(jsonify({"msg": "Token is expired."}), 400)
        except jwt.exceptions.DecodeError:
            return make_response(jsonify({"msg": "Error decoding token."}), 400)
        
    return wrapper

def generate_token(duration: int, payload: dict, key: str) -> str:
    """Takes care of generating a token.
    
    :param duration: indicates the duration of the token in seconds
    :param payload: dict that contains the claims
    :param key: the key to encrypt the token, default to the secret_key of the app
    :raises KeyError: if the payload does not contain the key "exp"
    :return: the JWT 
    """
    payload["exp"] += datetime.timedelta(seconds=duration) 
    token = jwt.encode(payload, key, algorithm="HS256")
    return token

@app.route("/", methods=["GET"])
def homepage():
    return "This is an unprotected route."

@app.route("/user", methods=["GET"])
@token_required
def homepage_user(user):
    return "Welcome {}!".format(user["username"])

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        email = data["email"]
        password = data["password"]

        if user["email"] == email and user["password"] == password:
            payload = {"iat": datetime.datetime.utcnow(), "exp": datetime.datetime.utcnow(), "email": email}
            access_token = generate_token(access_token_lifetime, payload, key)
            refresh_token = generate_token(refresh_token_lifetime, payload, key)
            return make_response(jsonify({"token": access_token, "refresh_token": refresh_token}), 200)
        return make_response(jsonify({"msg": "Bad username or password"}), 401)
    
    except KeyError:
        return make_response(jsonify({"msg": "Bad request"}), 400)

@app.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    
    try:
        refresh_token = data["refresh_token"]
        decoded = jwt.decode(refresh_token, key, algorithms="HS256")
        payload = {"iat": datetime.datetime.utcnow(), "exp": datetime.datetime.utcnow(), "email": decoded["email"]}
        return make_response(jsonify({"token": generate_token(refresh_token_lifetime, payload, key), "refresh_token": generate_token(refresh_token_lifetime, payload, key)}), 200)
    
    except KeyError:
        return make_response(jsonify({"msg": "Refresh token is missing."}), 400)
    except jwt.exceptions.ExpiredSignatureError:
        return make_response(jsonify({"msg": "Token is expired."}), 400)
    except jwt.exceptions.DecodeError:
        return make_response(jsonify({"msg": "Error decoding token."}), 400)

if __name__ == "__main__":
    app.run(debug=True)
