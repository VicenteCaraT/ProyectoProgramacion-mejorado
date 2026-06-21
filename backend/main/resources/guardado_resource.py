from flask_restful import Resource
from flask import request, jsonify
from main.auth.decorators import role_required, handle_errors
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.services import GuardadoService
from main.dtos import GuardadoDTO
from marshmallow import ValidationError
from main.schemas import GuardadoSchema
from .helpers import paginated_response

class Guardado(Resource):
    
    @handle_errors
    @jwt_required()
    def get(self, id):
        guardado = GuardadoService.get_by_id(id)
        return GuardadoDTO.full(guardado)
    
    @handle_errors
    @jwt_required()
    def delete(self, id):
        GuardadoService.delete(id)
        return '', 204
    
class Guardados(Resource):
    
    @handle_errors
    @jwt_required()
    def get(self):
        return paginated_response(GuardadoService, GuardadoDTO, 'guardados',
            idUsuario="idUsuario", libro_id="libro_id")
    
    @handle_errors
    @jwt_required()
    def post(self):
        schema = GuardadoSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as e:
            return {"message": "Datos inválidos", "errors": e.messages}, 422
        guardado = GuardadoService.create(get_jwt_identity(), data["libro"])
        return {
            "message": "Libro guardado exitosamente.",
            "guardado": GuardadoDTO.full(guardado)
        }, 201