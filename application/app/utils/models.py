from datetime import datetime
from .. import db


class BaseModel(object):
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    class DoesNotExists(Exception):
        pass

    @classmethod
    def get_by(cls, **kwargs):
        query = cls.query.filter_by(**kwargs)
        if query.count() != 1:
            raise cls.DoesNotExists
        return query.first()
