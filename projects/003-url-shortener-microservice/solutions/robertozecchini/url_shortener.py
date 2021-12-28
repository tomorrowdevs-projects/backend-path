#!/usr/bin/env python3

from flask import Flask, jsonify, request
import url_collection

app = Flask(__name__)
urls = url_collection.UrlCollection()

@app.route('/api/shorturl', methods = ['POST'])
def shorturl():
    raw_data = request.get_data()
    shorturl = urls.add_url(raw_data.decode('UTF-8'))
    if shorturl == 0:                   #invalid url
        return jsonify({'error': 'invalid url'})
    else:
        return jsonify({'original_url': str(urls.get_original(shorturl)), 'short_url': shorturl})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 