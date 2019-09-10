import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta

from auth.security import authenticate, identity
from items.resources import Item, Items
from auth.resources import Users
from auth.resources import UserRegister
from stores.resources import Store
from stores.resources import Stores

# Initialize the application
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"
)
app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=5)

app.secret_key = '388b38324541a8db402895f8ad084561c48e1af163c936d3'

# Initialize the API
api = Api(app)

# Initialize the JWT manager
jwt = JWT(app, authenticate, identity)

# Configure the URLS

# Users
api.add_resource(Users, "/users")
api.add_resource(UserRegister, "/register")

# Stores
api.add_resource(Store, "/store/<string:name>")
api.add_resource(Stores, "/stores")

# Items
api.add_resource(Item, "/item/<string:name>")
api.add_resource(Items, "/items")


if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(host="0.0.0.0")
