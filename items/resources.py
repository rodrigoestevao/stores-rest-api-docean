from http import HTTPStatus as status
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_jwt import jwt_required
from items import models


class Item(Resource):

    @staticmethod
    def _parser():
        parser = RequestParser()
        parser.add_argument(
            "price",
            type=float,
            required=True,
            help="This field cannot be left blank!"
        )
        parser.add_argument(
            "store_id",
            type=int,
            required=True,
            help="Every item needs a store associated!"
        )
        return parser

    @jwt_required()
    def get(self, name):
        item = models.Item.find_by_name(name)

        if item is not None:
            res = (item.json(), status.OK)
        else:
            res = ({"message": "Object not found!"}, status.NOT_FOUND)

        return res

    def post(self, name):
        item = models.Item.find_by_name(name)

        if item is None:
            data = self._parser().parse_args()
            item = models.Item(name, **data).save()
            res = (item.json(), status.CREATED)
        else:
            msg = f"An object with name {name} already exists"
            res = ({"message": msg}, status.BAD_REQUEST)

        return res

    def put(self, name):
        item = models.Item.find_by_name(name)

        if item is not None:
            data = self._parser().parse_args()
            item.price = data["price"]
            res = (item.save().json(), status.OK)
        else:
            msg = f"Could not find an object with name {name}."
            res = ({"message": msg}, status.NOT_FOUND)

        return res

    def delete(self, name):
        item = models.Item.find_by_name(name)

        if item is not None:
            if item.delete():
                res = status.NO_CONTENT
            else:
                res = ({"message": "Fail to delete"}, status.BAD_REQUEST)
        else:
            msg = f"Could not find an object with name {name}."
            res = ({"message": msg}, status.NOT_FOUND)

        return res


class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in models.Item.all()]}
