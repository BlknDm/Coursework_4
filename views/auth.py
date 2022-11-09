from flask import request
from flask_restx import Resource, Namespace, abort

from implemented import user_service
from service.auth import generate_tokens, approve_refresh_token

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

        token = generate_tokens(email, password)

        if not token:
            return {"error": "Неверный логин или пароль"}

        return token, 201

    def put(self):
        req_json = request.json
        refresh_token = req_json.get('refresh_token')

        if refresh_token is None:
            return {"error": "Токен просрочен"}, 400

        tokens = approve_refresh_token(refresh_token)

        return tokens, 201
