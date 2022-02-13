from encodings import utf_8
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from time import *
from dateutil.parser import *
import json


class RequestHandler(BaseHTTPRequestHandler):
    """A class that creates an object which handles the HTTP request"""

    def date_now(self):
        """
        A method that create a response to an empty request
        with the actual date and time
        """
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.utc_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.unix_date = datetime.timestamp(datetime.now())
        self.wfile.write(
            bytes(json.dumps({'unix': self.unix_date, 'utc': self.utc_date}),
                  'utf-8'))

    def requested_date_utc(self, date):
        """A method that create a response to an /api/<unix_timestamp>"""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.utc_date = date.strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.unix_date = datetime.timestamp(date)
        self.wfile.write(
            bytes(json.dumps({'unix': self.unix_date, 'utc': self.utc_date}),
                  'utf-8'))

    def requested_date_unix(self, date):
        """A method that create a response to an /api/<date>"""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.utc_date = datetime.fromtimestamp(
            date).strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.wfile.write(
            bytes(json.dumps({'unix': date, 'utc': self.utc_date}), 'utf-8'))

    def do_GET(self):
        "A get method that return a json object with a Unix key and a utc key"
        if self.path == '/api/':
            return self.date_now()
        else:
            try:
                if self.path[5:].isnumeric():
                    return self.requested_date_unix(int(self.path[5:]))
                else:
                    date = parse(self.path[5:].replace("%20", "-"))
            except ParserError or TypeError:
                return self.wfile.write(
                    bytes(json.dumps({'error': 'invalid date'}), 'utf-8'))
            else:
                return self.requested_date_utc(date)


def main():
    PORT = 8000
    server = HTTPServer(('', PORT), RequestHandler)
    print(f'Server running in port {PORT} ')
    server.serve_forever()


if __name__ == '__main__':
    main()
