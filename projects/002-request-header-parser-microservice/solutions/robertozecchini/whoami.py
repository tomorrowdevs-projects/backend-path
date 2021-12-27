#!/usr/bin/env python3

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/whoami')
def whoami():
    pass

if __name__ == '__main__':
    app.run(debug=True)