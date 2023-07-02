from flask import Flask

from operations import addition, subtraction, multiplication, division

app = Flask(__name__)

app.register_blueprint(addition.bp, url_prefix="/addition")
app.register_blueprint(subtraction.bp, url_prefix="/subtraction")
app.register_blueprint(multiplication.bp, url_prefix="/multiplication")
app.register_blueprint(division.bp, url_prefix="/division")


if __name__ == "__main__":
    app.run(debug=True)