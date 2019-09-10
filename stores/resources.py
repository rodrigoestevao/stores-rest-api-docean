from http import HTTPStatus as status
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_jwt import jwt_required
from stores import models


class Store(Resource):

    def _parser(self):
        return RequestParser()

    @jwt_required()
    def get(self, name):
        store = models.Store.find_by_name(name)

        if store is not None:
            res = (store.json(), status.OK)
        else:
            res = ({"message": "Object not found!"}, status.NOT_FOUND)

        return res

    @jwt_required()
    def post(self, name):
        store = models.Store.find_by_name(name)

        if store is None:
            store = models.Store(name).save()
            res = (store.json(), status.CREATED)
        else:
            msg = f"An object with name {name} already exists"
            res = ({"message": msg}, status.BAD_REQUEST)

        return res

    @jwt_required()
    def delete(self, name):
        item = models.Store.find_by_name(name)

        if item is not None:
            if item.delete():
                res = status.NO_CONTENT
            else:
                res = ({"message": "Fail to delete"}, status.BAD_REQUEST)
        else:
            msg = f"Could not find an object with name {name}."
            res = ({"message": msg}, status.NOT_FOUND)

        return res


class Stores(Resource):

    @jwt_required()
    def get(self):
        return {"stores": [store.json() for store in models.Store.all()]}