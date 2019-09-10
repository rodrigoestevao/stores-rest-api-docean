from http import HTTPStatus as status
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from auth import models


class UserRegister(Resource):

    @staticmethod
    def _parser():
        parser = RequestParser()
        fields = ["username", "password"]
        for field in fields:
            parser.add_argument(
                field,
                type=str,
                required=True,
                help=f"The {field} cannot be blank!"
            )
        return parser

    def post(self):
        data = self._parser().parse_args()

        user = models.User.find_by_username(data["username"])

        if user is None:
            user = models.User(**data).save()
            res = (user.json(), status.CREATED)
        else:
            msg = f"A user with name {data['username']} already exists"
            res = ({"message": msg}, status.BAD_REQUEST)

        return res


class Users(Resource):

    def get(self):
        return {"users": [user.json() for user in models.User.all()]}
