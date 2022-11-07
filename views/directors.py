from flask_restx import Resource, Namespace

from decorators import auth_required
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        directors = director_service.get_all()
        return directors, 200


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        director = director_service.get_item_by_id(did)
        return director, 200
