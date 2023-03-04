from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from implemented import movie_service
from utils import auth_required, admin_required

movie_ns = Namespace('movies')
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

@movie_ns.route('/')
class MovieView(Resource):
    @auth_required
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        year = request.args.get('year')
        filters = {
            'director_id': director_id,
            'genre_id': genre_id,
            'year': year,
        }

        all_movies = movie_service.get_all(filters)

        return movies_schema.dump(all_movies, many=True), 200

    @admin_required
    def post(self):
        req_json = request.json
        movie_service.create(req_json)

        return '', 201

@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    @auth_required
    def get(self, mid: int):
        movie = movie_service.get_one(mid)
        return movie_schema.dump(movie), 200

    @admin_required
    def put(self, mid: int):
        req_json = request.json
        req_json['id'] = mid

        movie_service.update(req_json)

        return '', 204

    @admin_required
    def delete(self, mid: int):
        movie_service.delete(mid)

        return '', 204
