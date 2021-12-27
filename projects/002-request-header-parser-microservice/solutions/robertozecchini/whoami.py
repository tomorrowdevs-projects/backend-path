#!/usr/bin/env python3

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/whoami')
def whoami():
    whoami = {}
    whoami['ip'] = request.remote_addr
    whoami['language'] = request.headers.get('Accept-Language', 'n.a.')
    whoami['software'] = request.headers.get('User-Agent', 'n.a.')
    return jsonify(whoami)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)