from flask_restful import Resource
from flask import request, jsonify
from datetime import datetime, timedelta
from main.auth.decorators import role_required, handle_errors
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from main.services import PrestamoService
from main.dtos import PrestamoDTO
from marshmallow import ValidationError
from main.schemas import PrestamoSchema
from .helpers import paginated_response


class Prestamo(Resource):
    
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def get(self, id):
        prestamo = PrestamoService.get_by_id(id)
        return PrestamoDTO.full(prestamo)

    @handle_errors
    @role_required(roles=["Admin"])
    def put(self, id):
        prestamo = PrestamoService.update(id, request.get_json())
        return{"message": "Préstamo actualizado correctamente.", "prestamo": PrestamoDTO.full(prestamo)}, 200
    
    @handle_errors
    @role_required(roles=["Admin"])
    def delete(self, id):
        PrestamoService.delete(id)
        return '', 204
    
class Prestamos(Resource):
    
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def get(self):
        return paginated_response(PrestamoService, PrestamoDTO, 'prestamos',
            idUsuario="idUsuario", inicio_prestamo="inicio_prestamo",
            fin_prestamo="fin_prestamo", cant_libros="cant_libros",
            libro_id="libro_id", titulo="titulo", estado="estado",
            nombre_usuario="nombre_usuario")
        
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def post(self):
        schema = PrestamoSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as e:
            return {"message": "Datos inválidos", "errors": e.messages}, 422
        prestamo = PrestamoService.create(data)
        return {"message": "Préstamo creado exitosamente.", "prestamo": PrestamoDTO.full(prestamo)}, 201
        
    @handle_errors
    @role_required(roles=["Admin"])
    def patch(self):
        cambios = PrestamoService.expire_overdue()
        return {"message": f"{cambios} préstamos vencidos fueron marcados como 'Terminados'."}, 200
        
if __name__ == '__main__':
    pass