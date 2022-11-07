from dao.model.user import User

from setup_db import db


class UserDAO:
    def __init__(self, session: db):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_data):
        res = User(**user_data)
        self.session.add(res)
        self.session.commit()
        return res

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_data):
        user = self.get_one(user_data.get("id"))
        user.email = user_data.get("email")
        user.password = user_data.get("password")
        user.name = user_data.get("name")
        user.surname = user_data.get("surname")
        user.favourite_genre = user_data.get("favourite_genre")

        self.session.add(user)
        self.session.commit()

    def get_user_by_email(self, email):
        return self.session.query(User).filter(User.email == email).one_or_none()
