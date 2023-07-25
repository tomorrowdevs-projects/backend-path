from flask import Flask

from views import index, auth


app = Flask(__name__)
app.config.from_object("config")

app.register_blueprint(index.bp, url_prefix="/")
app.register_blueprint(auth.bp, url_prefix="/auth")


if __name__ == "__main__":
    app.run(debug=True)
