from flask_restful import Resource
from flask import request, jsonify
from main.auth.decorators import role_required, handle_errors
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.services import ReseñaService
from main.dtos import ReseñaDTO
from .helpers import paginated_response


class Reseña(Resource):
    
    @handle_errors
    @jwt_required(optional=True)
    def get(self, id):
        reseña = ReseñaService.get_by_id(id)
        return ReseñaDTO.full(reseña)
    
    @handle_errors
    @role_required(roles=["Usuario", "Admin"])
    def put(self, id):
        reseña = ReseñaService.get_by_id(id)
        current_user_id = get_jwt_identity()
        if int(current_user_id) != int(reseña.fk_idUser) and "Admin" not in get_jwt().get('rol', []):
            return {"message": "No tiene permiso para modificar la reseña de este usuario"}
        reseña = ReseñaService.update(id, request.get_json())
        return {"message": f"Reseña con ID {id} actualizada correctamente.", "reseña": ReseñaDTO.full(reseña)}, 200
                
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def delete(self, id):
        current_user_id = get_jwt_identity()
        reseña = ReseñaService.get_by_id(id)
        if int(current_user_id) != int(reseña.fk_idUser) and "Admin" not in get_jwt().get('rol', []):
            return {"message": "No tiene permisos para borrar esta reseña"}, 403
        ReseñaService.delete(id)
        return '', 204
        
class Reseñas(Resource):
    # @jwt_required(optional=True)
    @handle_errors
    def get(self):
        return paginated_response(ReseñaService, ReseñaDTO, 'reseñas',
            nroValoracion="nroValoracion", ordenValoracion="ordenValoracion",
            idUserPost="idUserPost", fechaReseña="fechaReseña",
            idLibro="idLibro", nombre_usuario="nombre_usuario",
            titulo_libro="titulo_libro")
        
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def post(self):
        reseña = ReseñaService.create(request.get_json())
        return {"message": "Reseña creada exitosamente.", "reseña": ReseñaDTO.full(reseña)}, 201
    
if __name__ == '__main__':
    pass