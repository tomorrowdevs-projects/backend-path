import os

from flask import Flask

from views import auth, index


def create_app(env: str) -> Flask:
    """Takes care of creating the app by configuring it according to the type of environment and registering the
    blueprints.

    :param env: the environment for which the app is to be created, for example config.DevelopmentConfig if it is a
    development environment or config.TestingConfig if it is a test environment
    :return: the created Flask app
    """
    app = Flask(__name__)
    app.config.from_object(env)
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(index.bp, url_prefix="/")
    return app


if __name__ == '__main__':
    # when run locally, https verification is disabled, this is because oauth2 requires https to be used
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app = create_app(env='config.DevelopmentConfig')
    app.run()
