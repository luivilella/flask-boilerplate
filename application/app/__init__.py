from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .config import config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'


def create_app(config_name='default'):
    app = Flask(__name__)
    app_conf = config[config_name]

    app.config.from_object(app_conf)
    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .auth.views import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
