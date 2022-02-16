from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self) -> None:
        pass

    def response(self):
        pass

    def short_url_redirect(self):
        pass

    def url_handler(self):
        pass


if __name__ == "__main__":
    PORT = 8000
    server = HTTPServer(('', PORT), RequestHandler)
    print(f"Server running on {PORT}")

    server.serve_forever()