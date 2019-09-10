from db import db


class Store(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship("Item", backref="store", lazy="dynamic")

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            "name": self.name,
            "items": [item.json() for item in self.items.all()]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

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

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            print(f"Error when removing object: {e}")
            db.session.rollback()
            res = False
        else:
            res = True

        return res
