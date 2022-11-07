from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from decorators import auth_required
from implemented import user_service
from implemented import auth_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        all_users = user_service.get_all()
        res = UserSchema(many=True).dump(all_users)
        return res, 200

@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        b = user_service.get_one(uid)
        res = UserSchema().dump(b)
        return res, 200

    @auth_required
    def patch(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204

@user_ns.route('/password/')
class UserPasswordView(Resource):
    @auth_required
    def put(self):
        password_1 = request.json.get('password_1')
        password_2 = request.json.get('password_2')
        header = request.headers['Authorization']
        email = auth_service.get_email_from_header(header)

        return auth_service.change_the_password(email, password_1, password_2)
