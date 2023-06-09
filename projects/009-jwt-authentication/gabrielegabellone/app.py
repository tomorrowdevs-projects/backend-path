import jwt
import datetime

from flask import Flask, request, jsonify, make_response

from jwt_auth.token import generate_token, extract_token

app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"

user = {"email": "test@email.com", "password": "test", "username": "test"}
access_token_lifetime = 3
refresh_token_lifetime = 5
key = app.config["SECRET_KEY"]

def token_required(f):
    def wrapper():
        data = request.get_json()

        try:
            token = extract_token(data)
        except Exception:
            return make_response(jsonify({"msg" : "Token is missing."}), 401)
  
        try:
            data = jwt.decode(token, key, algorithms="HS256")
            if data["email"] == user["email"]:
                return f(user)
        except jwt.exceptions.ExpiredSignatureError:
            return make_response(jsonify({"msg": "Token is expired."}), 400)
        except jwt.exceptions.DecodeError:
            return make_response(jsonify({"msg": "Error decoding token."}), 400)
        
    return wrapper


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
            return make_response(jsonify({"token": generate_token(access_token_lifetime, payload, key), "refresh_token": generate_token(refresh_token_lifetime, payload, key)}), 200)
        return make_response(jsonify({"msg": "Bad username or password"}), 401)
    
    except KeyError:
        return make_response(jsonify({"msg": "Bad request"}), 400)

@app.route("/refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    
    try:
        refresh_token = data["refresh_token"]
        decoded = jwt.decode(refresh_token, app.config['SECRET_KEY'], algorithms="HS256")
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
