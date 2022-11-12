import hashlib

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_user_by_email(self, email):
        return self.dao.get_user_by_email(email)

    def get_all(self):
        users = self.dao.get_all()
        return users

    def create(self, user_data):
        user_data["password"] = self.get_hash(user_data["password"])
        return self.dao.create(user_data)

    def delete(self, uid):
        self.dao.delete(uid)

    def patch(self, user_data):
        self.dao.update(user_data)

    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")
