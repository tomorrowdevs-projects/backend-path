from flask import Flask, jsonify, request
import jwt
import datetime

key = "our_really_secret_key"
users = {
        "user1": "password1",
        "user2": "password2"
        }
access_duration = 3
refresh_duration = 120

app = Flask(__name__)

def create_token(username, t_type = "access", duration = 5):
    payload = {
              "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds = duration),
              "iat": datetime.datetime.utcnow(),
              "id": username,
              "type": t_type
              }
    encoded = jwt.encode(payload, key, algorithm = "HS256")
    return encoded

@app.route("/login", methods = ["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username in users and users[username] == password:
        access_token = create_token(username, "access", access_duration)
        refresh_token = create_token(username, "refresh", refresh_duration)
        return jsonify({"access_token": access_token, "refresh_token": refresh_token})
    else:
        return jsonify({"error": "invalid username or password"})

@app.route("/refresh", methods = ["GET"])
def refresh():
    token = None
    if "x-access-tokens" in request.headers:
        token = request.headers["x-access-tokens"]
    elif "authorization" in request.headers:
        token = request.headers["authorization"]
    if not token:
        return jsonify({"error": "missing token"})
    elif token.startswith("Bearer "):
        token = token[7:]
    try:
        payload = jwt.decode(token, key, algorithms = ["HS256"])
        t_type = payload["type"]
        if t_type != "refresh":
            return jsonify({"error": "Invalid token type"})
        user = payload["id"]
        if user in users:
            access_token = create_token(user, "access", access_duration)
            refresh_token = create_token(user, "refresh", refresh_duration)
            return jsonify({"access_token": access_token, "refresh_token": refresh_token})
        else:
            return jsonify({"error": "Invalid token id"})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Signature expired"})
    except:
        return jsonify({"error": "Invalid token"})

@app.route("/", methods = ["GET"])
def hello_user():
    token = None
    if "x-access-tokens" in request.headers:
        token = request.headers["x-access-tokens"]
    elif "authorization" in request.headers:
        token = request.headers["authorization"]
    if not token:
        return jsonify({"error": "missing token"})
    elif token.startswith("Bearer "):
        token = token[7:]
    try:
        payload = jwt.decode(token, key, algorithms = ["HS256"])
        t_type = payload["type"]
        if t_type != "access":
            return jsonify({"error": "Invalid token type"})
        user = payload["id"]
        if user in users:
            return jsonify({"Hello": user})
        else:
            return jsonify({"error": "Invalid token id"})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Signature expired"})
    except:
        return jsonify({"error": "Invalid token"})

if __name__ == "__main__":
    app.run()