import jwt
from flask import request
from flask_restx import abort

from constants import PWD_HASH_SALT


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        try:
            jwt.decode(token, PWD_HASH_SALT, algorithms=['HS256'])
        except Exception as e:
            print('JWT Decode error')
            abort(401)
        return func(*args, **kwargs)
    return wrapper
