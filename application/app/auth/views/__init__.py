from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import users  # noqa: E402, F401
