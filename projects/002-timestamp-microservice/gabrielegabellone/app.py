from flask import Flask
from flasgger import Swagger

from microservices.date_service import bp

app = Flask(__name__)
app.config['SWAGGER'] = {
    'openapi': '3.0.0'
}
template = {
  "info": {
    "title": "Timestamp Microservice",
  }
}
swagger = Swagger(app, template=template)

app.register_blueprint(bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
    