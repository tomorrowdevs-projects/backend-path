from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flasgger import Swagger

from models import db, User
from views import index, auth


def register_blueprint_and_add_login_manager(app: Flask):
    """It takes care of registering the blueprints and adding the login manager to the app.

    :param app: the reference app Flask
    """
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(index.bp, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: int) -> User:
        """Manages the loading of the user in the login session.

        :param user_id: the id of the user who needs to log in
        """
        return db.session.get(User, user_id)


def create_app() -> Flask:
    """Goes to create the flask app.

    :return: the Flask app with the configurations set in the config file
    """
    app = Flask(__name__)
    app.config.from_object("config")
    db.init_app(app)
    migrate = Migrate(app, db)
    register_blueprint_and_add_login_manager(app)
    template = {
        "info": {
            "title": "Role Based Access Control",
        }
    }
    swagger = Swagger(app, template=template)
    return app


def create_test_app() -> Flask:
    """Goes to create a flask app purely for testing.

    :return: the Flask app configured for testing purposes
    """
    app = Flask(__name__)
    app.config.from_object("config_tests")
    db.init_app(app)
    register_blueprint_and_add_login_manager(app)
    app.app_context().push()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run()



