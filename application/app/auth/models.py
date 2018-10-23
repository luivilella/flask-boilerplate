from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .. import db
from .. import login_manager
from ..utils.models import BaseModel


class User(BaseModel, UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(64), unique=True, index=True, nullable=False
    )
    passwd = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(255), default='')

    def __repr__(self):
        return f'{self.id}/{self.username}'

    @property
    def password(self):
        raise ValueError

    @password.setter
    def password(self, password):
        self.passwd = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwd, password)

    @staticmethod
    def _format_username(username):
        return username.strip().lower()

    @classmethod
    def create(cls, username, password, fullname='', auto_commit=True):
        user = User()
        user.username = cls._format_username(username)
        try:
            User.get_by(username=user.username)
            return
        except User.DoesNotExists:
            pass
        user.password = password
        user.fullname = fullname
        db.session.add(user)
        if auto_commit:
            db.session.commit()

        return user

    @classmethod
    def get_by_login_and_password(cls, username, password):
        try:
            user = User.get_by(username=cls._format_username(username))
        except User.DoesNotExists:
            return

        if not user.check_password(password):
            return

        return user


class AnonymousUser:
    @property
    def is_active(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return None

    def __repr__(self):
        return 'AnonymousUser'


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
