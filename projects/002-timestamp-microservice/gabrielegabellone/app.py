from flask import Flask

from microservices.date_service import bp


app = Flask(__name__)
app.register_blueprint(bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
    