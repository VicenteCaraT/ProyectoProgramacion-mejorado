from flask_restful import Resource
from flask import request, jsonify
from main.auth.decorators import role_required, handle_errors
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.services import GuardadoService
from main.dtos import GuardadoDTO

class Guardado(Resource):
    
    @handle_errors
    @jwt_required()
    def get(self, id):
        guardado = GuardadoService.get_by_id(id)
        return GuardadoDTO.full(guardado, guardado.fk_user_guardado, guardado.fk_libro_guardado)
    
    @handle_errors
    @jwt_required()
    def delete(self, id):
        GuardadoService.delete(id)
        return '', 204
    
class Guardados(Resource):
    
    @handle_errors
    @jwt_required()
    def get(self):
        filters = {
            "page": int(request.args.get("page", 1)),
            "per_page": int(request.args.get("per_page", 10)),
            "idUsuario": request.args.get("idUsuario"),
            "libro_id": request.args.get("libro_id"),
        }
        filters = {k: v for k, v in filters.items() if v is not None}
        result = GuardadoService.get_all(filters)
        return jsonify({
            'guardados': [GuardadoDTO.full(g, g.fk_user_guardado, g.fk_libro_guardado) for g in result.items],
            'total': result.total,
            'pages': result.pages,
            'page': int(request.args.get("page", 1))
        })
    
    @handle_errors
    @jwt_required()
    def post(self):
        data = request.get_json()
        libro_id = data.get("libro")
        if not libro_id:
            return {"message": "Falta el ID del libro"}, 400
        guardado = GuardadoService.create(get_jwt_identity(), libro_id)
        return {
            "message": "Libro guardado exitosamente.",
            "guardado": GuardadoDTO.full(guardado, guardado.fk_user_guardado, guardado.fk_libro_guardado)
        }, 201