class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'random secret key'
    CLIENT_SECRET_JSON_PATH = 'client_secret.json'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    CLIENT_SECRET_JSON_PATH = 'tests/mock_client_secret.json'
