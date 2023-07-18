from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    """View function that redirects to an html page with a form to upload a file."""
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """View function that returns a JSON object with the name, size and type of file input into the request."""
    file = request.files["upfile"]
    file_name = file.filename
    file_size = len(file.read())
    file_type = file.content_type
    return jsonify({"name": file_name, "size": file_size, "type": file_type})


if __name__ == "__main__":
    app.run(debug=True)
