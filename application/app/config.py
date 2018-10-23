from environs import Env
from dotenv import load_dotenv
from dotenv import find_dotenv


load_dotenv(find_dotenv())
env = Env()


class Config(object):
    SECRET_KEY = env('FLASK_SECRET_KEY', 'cy4xJ4ONjrjAWHW2FANV')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_DATABASE_URI = env('FLASK_DATABASE_URI', 'sqlite://')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
