from flask import Flask, request

# A request to /api/whoami should return a JSON object with:
#  - your IP address in the ipaddress key.
#  - your preferred language in the language key.
#  - your software in the software key.

app = Flask(__name__)

@app.route("/api/whoami")
def index():
    
    res = {"IP": request.remote_addr,
           "software": request.headers["User-Agent"],
          "language": request.headers.get('Accept-Language', 'Language not found')
            }
    return res


if __name__ == "__main__":
    app.run(debug=True)