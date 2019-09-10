from functools import partial

from db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {"user": {"username": self.username, "password": "XXXXX"}}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def all(cls):
        return cls.query.all()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(f"Error when saving object: {e}")
            db.session.rollback()
            res = None
        else:
            res = self

        return res
