from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_user():
    user = "Pippo"
    return jsonify({'Hello': user})