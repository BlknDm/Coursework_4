from flask_restx import Resource, Namespace

from decorators import auth_required
from implemented import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        genres = genre_service.get_all()
        return genres, 200


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        genre = genre_service.get_item_by_id(gid)
        return genre, 200
