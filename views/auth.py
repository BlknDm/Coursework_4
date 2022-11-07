from flask import request
from flask_restx import Resource, Namespace, abort

from implemented import auth_service
from implemented import user_service

auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class AuthRegisterView(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email and not password:
            abort(400)

        user_service.create(data)

        return '', 201


@auth_ns.route('/login/')
class AuthLoginView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get('email')
        password = req_json.get('password')

        if not email and not password:
            abort(400)

        token = auth_service.auth_user(email, password)

        if not token:
            return {"error": "Неверный логин или пароль"}

        return token, 201

    def put(self):
        req_json = request.json
        refresh_token = req_json.get('refresh_token')

        if refresh_token is None:
            return {"error": "Токен просрочен"}, 400

        tokens = user_service.check_refresh_token(refresh_token)

        return tokens, 201
