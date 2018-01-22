from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import json as _json

db = SQLAlchemy()

class Model(object):
    @classmethod
    def get(cls, primary_key):
        return cls.query.get(primary_key)

    def put(self):
        db.session.add(self)

    @classmethod
    def commit(self):
        db.session.commit()

    @classmethod
    def rollback(self):
        db.session.rollback()

    def delete(self):
        db.session.delete(self)

    def save(self):
        try:
            self.put()
            self.commit()
        except Exception:
            self.rollback()
            raise

    def __json__(self):
        data = {}
        for k, v in vars(self).items():
            if k.startswith('_'):
                continue
            if isinstance(v, datetime):
                v = v.strftime("%Y%m%d%H%M%S")
            data[k] = v
        return data

class JSONEncoder(_json.JSONEncoder):
    def default(self, o):
        if isinstance(o, db.Model):
            return o.__json__()
        if type(o) == bytes:
            return o.decode('utf-8')
        return _json.JSONEncoder.default(self, o)
