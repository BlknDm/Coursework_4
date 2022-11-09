import base64
import calendar
import datetime
import hashlib
import hmac
from flask import abort
import jwt
from constants import ALGO, PWD_HASH_ITERATIONS, PWD_HASH_SALT
from implemented import user_service
from setup_db import db


def generate_tokens(email, password):
    user = user_service.get_user_by_email(email)

    if user is None:
        raise abort(404)

    data = {
        'user_email': user.email
    }

    min10 = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
    data['exp'] = calendar.timegm(min10.timetuple())
    access_token = jwt.encode(data, PWD_HASH_SALT, algorithm=ALGO)

    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data['exp'] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, PWD_HASH_SALT, algorithm=ALGO)

    return {'access_token': access_token,
            'refresh_token': refresh_token}


def check_password(db_hash, password):
    decoded_digest = base64.b64decode(db_hash)

    hash_digest = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    )

    return hmac.compare_digest(decoded_digest, hash_digest)


def approve_refresh_token(refresh_token):
    try:
        data = jwt.decode(jwt=refresh_token, key=PWD_HASH_SALT, algorithms=[ALGO])

    except Exception as e:
        return f'{e}', 401

    email = data.get('user_email')

    return generate_tokens(email, None, is_refresh=True)


def get_email_from_header(header: str):

    token = header.split('Bearer ')[-1]
    data_dict = jwt.decode(token, PWD_HASH_SALT, ALGO)

    email = data_dict.get('user_email')

    return email


def change_the_password(user_email, pass1, pass2):

    user = user_service.get_user_by_email(user_email)

    db_pass = user.password

    is_confirmed = check_password(db_pass, pass1)

    if is_confirmed:

        user.password = user_service.get_hash(pass2)

        db.session.add(user)
        db.session.commit()

        return '', 204

    abort(401)
