from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from main.auth.decorators import role_required, handle_errors
from main.services import AutorService
from main.dtos import AutorDTO
from .helpers import paginated_response

class Autor(Resource):
    
    @handle_errors
    @jwt_required(optional=True)
    def get(self, id):
        autor = AutorService.get_by_id(id)
        return {"message": "Autor obtenido exitosamente", "autor": AutorDTO.full(autor)
        }, 200
    
    @handle_errors
    @role_required(roles=['Admin'])
    def put(self, id):
        autor = AutorService.update(id, request.get_json())
        return {"message": "Autor actualizado correctamente", "autor": AutorDTO.full(autor)
        }, 200
    
    @handle_errors
    @role_required(roles=['Admin'])
    def delete(self, id):
        AutorService.delete(id)
        return '', 204

class Autores(Resource):

    @handle_errors
    @jwt_required(optional=True)
    def get(self):
        return paginated_response(AutorService, AutorDTO, "autores", nombre="nombre", apellido="apellido", apodo="apodo")
        
    @handle_errors
    @role_required(roles=["Admin"])
    def post(self):
        autor = AutorService.create(request.get_json())
        return {"message": "Autor creado exitosamente", "autor": AutorDTO.full(autor)}, 201
    
    
if __name__ == '__main__':
    pass