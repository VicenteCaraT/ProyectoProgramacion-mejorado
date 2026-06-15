from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from main.auth.decorators import role_required, handle_errors
from main.services import AutorService
from main.dtos import AutorDTO

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
        filters = {
            "page": int(request.args.get("page", 1)),
            "per_page": int(request.args.get("per_page", 10)),
            "nombre": request.args.get("nombre"),
            "apellido": request.args.get("apellido"),
            "apodo": request.args.get("apodo"),
        }
        filters = {k: v for k, v in filters.items() if v is not None}
        result = AutorService.get_all(filters)
        return jsonify({
            'autores': [AutorDTO.full(a) for a in result.items],
            'total': result.total,
            'pages': result.pages,
            'page': int(request.args.get("page", 1))
        })
        
    @handle_errors
    @role_required(roles=["Admin"])
    def post(self):
        autor = AutorService.create(request.get_json())
        return {"message": "Autor creado exitosamente", "autor": AutorDTO.full(autor)}, 201
    
    
if __name__ == '__main__':
    pass