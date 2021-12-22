#!/usr/bin/env python3

import time
import datetime
import urllib.parse
from flask import Flask, jsonify
from dateutil.parser import parse

app = Flask(__name__)

#function that takes seconds from epoch and returns a json indicated the timestamp in milliseconds and a string representing the date in UTC
def unix2json(unix):
    utc = datetime.datetime.fromtimestamp(unix, tz=datetime.timezone.utc)
    unix = int(unix*1000)        #convert it in milliseconds
    return jsonify({'unix': unix, 'utc': utc})

#returns current time
@app.route('/api/')
def index():
    unix = time.time()
    return unix2json(unix)

#function that takes a date in human-readale format or in milliseconds from epoch and returns a json indicated the timestamp in milliseconds and a string representing the date in UTC
@app.route('/api/<date_string>', methods=['GET'])
def Date(date_string):
    date_string = urllib.parse.unquote(date_string)
    if date_string.isnumeric():
        unix = int(date_string) / 1000
        return unix2json(unix)
    elif date_string[0] == ':' and date_string[-1] == '?':
        date = date_string[1:-1]
        try:
            d = parse(date)
            unix = d.timestamp()
            return unix2json(unix)
        except ValueError:
            return jsonify({'error': "Invalid Date"})
    else:
        return jsonify({'error': "Invalid Date"})

if __name__ == '__main__':
    app.run(debug=True)
