from http import HTTPStatus
from cerberus import Validator
from flask import request
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from . import auth
from ..models import User
from ... import db
from ...utils.views import BaseView


def _user_to_dict(user):
    return {
        'id': user.id,
        'username': user.username,
        'fullname': user.fullname,
    }


class UserAPI(BaseView):
    new_user_schema = {
        'username': {'required': True, 'type': 'string'},
        'password': {'required': True, 'type': 'string', 'minlength': 8},
        'fullname': {'type': 'string'},
    }

    def all(self):
        users = []
        for user in User.query.all():
            users.append(_user_to_dict(user))
        return self.json_response(users)

    def detail(self, user_id):
        try:
            user = User.get_by(id=user_id)
        except User.DoesNotExists:
            return self.json_response({}, HTTPStatus.NOT_FOUND)

        return self.json_response(_user_to_dict(user))

    def get(self, user_id=None):
        if user_id:
            return self.detail(user_id)
        return self.all()

    def post(self):
        data = request.get_json()
        validator = Validator(self.new_user_schema)
        is_valid = validator.validate(data)
        if not is_valid:
            return self.json_response(validator.errors, HTTPStatus.BAD_REQUEST)

        user = User.create(**validator.normalized(data))
        if not user:
            return self.json_response(
                {'username': ['already exists']},
                HTTPStatus.CONFLICT
            )
        return self.json_response({'id': user.id}, HTTPStatus.CREATED)


user_view = UserAPI.as_view('users')
auth.add_url_rule('/users', view_func=user_view)
auth.add_url_rule('/users/<int:user_id>', view_func=user_view)


class AuthenticationAPI(BaseView):
    new_password_schema = {
        'password': {'required': True, 'type': 'string', 'minlength': 8},
        'fullname': {'type': 'string'},
    }

    login_schema = {
        'username': {'required': True, 'type': 'string'},
        'password': {'required': True, 'type': 'string'},
    }

    @login_required
    def get(self):
        if not self.logged_user.is_authenticated:
            return self.json_response({}, HTTPStatus.UNAUTHORIZED)
        return self.json_response(_user_to_dict(self.logged_user))

    def post(self):
        data = request.get_json()
        validator = Validator(self.login_schema)
        is_valid = validator.validate(data)
        if not is_valid:
            return self.json_response(validator.errors, HTTPStatus.BAD_REQUEST)

        user = User.get_by_login_and_password(**validator.normalized(data))
        if not user:
            return self.json_response(
                {
                    'username': ['invalid'],
                    'password': ['invalid'],
                },
                HTTPStatus.BAD_REQUEST
            )

        login_user(user)
        return self.json_response({'id': user.id})

    @login_required
    def put(self):
        data = request.get_json()
        validator = Validator(self.login_schema)
        is_valid = validator.validate(data)
        if not is_valid:
            return self.json_response(validator.errors, HTTPStatus.BAD_REQUEST)

        clean_data = validator.normalized(data)
        user = self.logged_user
        if 'fullname' in clean_data:
            user.fullname = clean_data['fullname']
        user.set_password(clean_data['password'])
        db.session.add(user)
        db.session.commit()

        return self.json_response({'id': user.id}, HTTPStatus.ACCEPTED)

    def delete(self):
        logout_user()
        return self.json_response({}, HTTPStatus.UNAUTHORIZED)


authentication_view = AuthenticationAPI.as_view('authentication')
auth.add_url_rule('/login', view_func=authentication_view)
