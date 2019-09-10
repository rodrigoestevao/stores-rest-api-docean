from werkzeug.security import safe_str_cmp

from auth.models import User


def authenticate(username, password):
    user = User.find_by_username(username)
    return user if user and safe_str_cmp(user.password, password) else None


def identity(payload):
    user_id = payload["identity"]
    return User.find_by_id(user_id)