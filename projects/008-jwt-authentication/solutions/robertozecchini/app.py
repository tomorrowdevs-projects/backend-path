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

class ErrMissingToken(Exception):
    pass

class ErrInvalidTokenType(Exception):
    pass

class ErrInvalidTokenId(Exception):
    pass

class ErrInvalidLogin(Exception):
    pass

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

def get_tokens(username):
    access_token = create_token(username, "access", access_duration)
    refresh_token = create_token(username, "refresh", refresh_duration)
    return {"access_token": access_token, "refresh_token": refresh_token}

def get_token_from_request(request):
    token = None
    if "x-access-tokens" in request.headers:
        token = request.headers["x-access-tokens"]
    elif "authorization" in request.headers:
        token = request.headers["authorization"]
    if not token:
        raise ErrMissingToken
    elif token.startswith("Bearer "):
        token = token[7:]
    return token

def verify_auth(request, requested_type):
    token = get_token_from_request(request)
    payload = jwt.decode(token, key, algorithms = ["HS256"])
    t_type = payload["type"]
    if t_type != requested_type:
        raise ErrInvalidTokenType
    user = payload["id"]
    if user in users:
        return user
    else:
        raise ErrInvalidTokenId

def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Signature expired"})
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"})
        except ErrInvalidLogin:
            return jsonify({"error": "Invalid username or password"})
        except ErrInvalidTokenId:
            return jsonify({"error": "Invalid token id"})
        except ErrInvalidTokenType:
            return jsonify({"error": "Invalid token type"})
        except ErrMissingToken:
            return jsonify({"error": "Missing token"})
        except:
            return jsonify({"error": "Something went wrong.."})
    inner_function.__name__ = func.__name__
    return inner_function

@app.route("/login", methods = ["POST"])
@exception_handler
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username in users and users[username] == password:
        return jsonify(get_tokens(username))
    else:
        raise ErrInvalidLogin

@app.route("/refresh", methods = ["GET"])
@exception_handler
def refresh():
    user = verify_auth(request, "refresh")
    return jsonify(get_tokens(user))

@app.route("/", methods = ["GET"])
@exception_handler
def hello_user():
    user = verify_auth(request, "access")
    return jsonify({"Hello": user})

if __name__ == "__main__":
    app.run()