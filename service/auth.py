import hashlib
from datetime import timedelta, datetime

import jwt

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO
from utils import get_hash


class AuthService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_tokens(self, data):
        min10 = datetime.utcnow() + timedelta(days=10)
        data['exp'] = int(min10.timestamp())
        access_token = jwt.encode(data, PWD_HASH_SALT)

        days130 = datetime.utcnow() + timedelta(days=130)
        data['exp'] = int(days130.timestamp())
        refresh_token = jwt.encode(data, PWD_HASH_SALT)

        return {'access_token': access_token, 'refresh_token': refresh_token}

    def auth_user(self, email, password):
        user = self.dao.get_user_by_email(email)

        if not user:
            return None

        hash_password = get_hash(password)

        if hash_password != user.password:
            return None

        data = {
            'email': user.email,
        }

        tokens = self.get_tokens(data)
        return tokens

    def check_refresh_token(self, refresh_token):
        try:
            data = jwt.decode(jwt=refresh_token, key=PWD_HASH_SALT, algorithms='HS256')
        except Exception as e:
            return None

        tokens = self.get_tokens(data)

        return tokens


