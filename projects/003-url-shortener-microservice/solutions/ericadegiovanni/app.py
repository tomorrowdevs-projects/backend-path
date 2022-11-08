from flask import Flask, jsonify, redirect, request
from urls import Urls

# You can POST a URL to /api/shorturl and get a JSON response with original_url and short_url properties.
# When you visit /api/shorturl/<short_url>, you will be redirected to the original URL.
# The URL must  follow the valid http://www.example.com format, if not return a JSON response { error: 'invalid url' }

app = Flask(__name__)
url = Urls()

@app.route("/api/shorturl", methods=["POST"])
def make_post():
    posted_url = request.get_data().decode()
    res = url.add_post(posted_url)
    return res
    

@app.route('/api/shorturl/<int:short_url>')
def get_url(short_url):

    try:
        original_url = url.url_list[short_url - 1]["original_url"]
        return redirect(f"{original_url}")
    except IndexError:
        return {"error": "invalid short-url"}


@app.route('/api/shorturl/all')
def get_urls():
    return jsonify(url.url_list)
    

if __name__ == '__main__':
    app.run(debug=True) 