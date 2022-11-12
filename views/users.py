from flask import request, abort
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from decorators import auth_required
from implemented import user_service
from service.auth import get_email_from_header, change_the_password

user_ns = Namespace('user')

user_schema = UserSchema()


@user_ns.route('/')
class UserView(Resource):
    @auth_required
    def get(self):
        req_header = request.headers['Authorization']

        email = get_email_from_header(req_header)

        if not email:
            abort(401)

        selected_user = user_service.get_user_by_email(email)

        return user_schema.dump(selected_user), 200

    @auth_required
    def patch(self):
        req_header = request.headers['Authorization']

        email = get_email_from_header(req_header)

        if not email:
            abort(401)

        req_data = request.json

        if not req_data:
            abort(401)

        req_data['email'] = email
        user_service.patch(req_data)

        return "", 204


@user_ns.route('/password/')
class UserPasswordView(Resource):
    @auth_required
    def put(self):
        password_1 = request.json.get('password_1')
        password_2 = request.json.get('password_2')
        header = request.headers['Authorization']
        email = get_email_from_header(header)

        return change_the_password(email, password_1, password_2)
