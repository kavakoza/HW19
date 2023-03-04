from flask_restx import Resource, Namespace
from flask import request

from dao.model.director import DirectorSchema
from implemented import director_service
from utils import auth_required, admin_required

director_ns = Namespace('directors')
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        all_directors = director_service.get_all()

        return directors_schema.dump(all_directors, many=True), 200

    @admin_required
    def post(self):
        req_json = request.json
        director_service.create(req_json)

        return '', 201


@director_ns.route('/<int:did>')
class GenreView(Resource):
    @auth_required
    def get(self, did: int):
        director = director_service.get_one(did)

        return director_schema.dump(director), 200

    @admin_required
    def put(self, did: int):
        req_json = request.json
        req_json['id'] = did

        director_service.update(req_json)

        return '', 204

    @admin_required
    def delete(self, did: int):
        director_service.delete(did)

        return '', 204