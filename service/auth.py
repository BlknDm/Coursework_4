import base64
import hashlib
import hmac
from datetime import timedelta, datetime

import jwt
from flask_restx import abort

from constants import PWD_HASH_SALT, ALGO, PWD_HASH_ITERATIONS
from dao.user import UserDAO
from implemented import user_service
from setup_db import db
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

    def check_password(db_hash, client_password):
        decoded_digest = base64.b64decode(db_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            client_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decoded_digest, hash_digest)

    def check_refresh_token(self, refresh_token):
        try:
            data = jwt.decode(jwt=refresh_token, key=PWD_HASH_SALT, algorithms=ALGO)
        except Exception as e:
            return None

        tokens = self.get_tokens(data)

        return tokens

    def get_email_from_header(header: str):

        token = header.split('Bearer ')[-1]
        data_dict = jwt.decode(token, PWD_HASH_SALT, ALGO)

        email = data_dict.get('user_email')

        return email

    def change_the_password(email, pass1, pass2):

        user = user_service.get_by_email(email)

        db_pass = user.password

        is_confirmed = email.check_password(db_pass, pass1)

        if is_confirmed:
            user.password = user_service.get_hash(pass2)

            db.session.add(user)
            db.session.commit()

            return '', 204

        abort(401)
