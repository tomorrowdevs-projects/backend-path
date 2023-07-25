from flask import Flask
from flasgger import Swagger

from views import index, auth


app = Flask(__name__)
app.config.from_object("config")

app.register_blueprint(index.bp, url_prefix="/")
app.register_blueprint(auth.bp, url_prefix="/auth")

template = {
    "info": {
        "title": "JWT Authentication"
    },
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    }
}

swagger = Swagger(app, template=template)


if __name__ == "__main__":
    app.run(debug=True)
