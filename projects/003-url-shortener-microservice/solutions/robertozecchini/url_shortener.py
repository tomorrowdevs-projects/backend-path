#!/usr/bin/env python3

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/shorturl')
def shorturl():
    shorturl = {}
    return jsonify(shorturl)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 