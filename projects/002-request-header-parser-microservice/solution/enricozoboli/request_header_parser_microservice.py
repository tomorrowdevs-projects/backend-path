from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class RequestHandler(BaseHTTPRequestHandler):
    """
    A class for create a request handler object, inheriting from BaseHTTPRequestHandler,
    to serve a response for a get request on localhost:8000/whoami endpoint.
    """

    def response(self):
        """
        Method that writes a json converted response for the client
        """
        return self.wfile.write(bytes(self.convert_to_json(), 'utf-8'))

    def convert_to_json(self):

        return json.dumps({
            self.client_address[0]: 'ipaddress',
            self.headers['Accept-Language']: 'language',
            self.headers['User-Agent']: 'software'
        })

    def do_GET(self):

        if self.path == '/whoami':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.response()


def main():
    PORT = 8000
    server = HTTPServer(('', PORT), RequestHandler)
    print(f'Server running on port {PORT}')

    server.serve_forever()


if __name__ == '__main__':
    main()
