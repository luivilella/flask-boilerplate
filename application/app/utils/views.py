
from http import HTTPStatus
from flask.views import MethodView
from flask import jsonify
from flask import request
from flask_login import current_user


class BaseView(MethodView):
    def json_response(self, data, status_code=HTTPStatus.OK):
        return jsonify(data), status_code

    @property
    def logged_user(self):
        return current_user
