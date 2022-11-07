from flask import request
from flask_restx import Resource, Namespace, abort

from decorators import auth_required
from implemented import movie_service

movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    @auth_required
    def get(self):
        data = {
            'status': request.args.get('status'),
            'page': request.args.get("page")
        }
        movies = movie_service.get_all(data)

        return movies, 200


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid):
        movie = movie_service.get_by_id(mid)

        if not movie:
            abort(404, message='Movie not found')

        return movie, 200
