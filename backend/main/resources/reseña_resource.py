from flask_restful import Resource
from flask import request, jsonify
from main.auth.decorators import role_required, handle_errors
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.services import ReseñaService
from main.dtos import ReseñaDTO


class Reseña(Resource):
    
    @handle_errors
    @jwt_required(optional=True)
    def get(self, id):
        reseña = ReseñaService.get_by_id(id)
        return ReseñaDTO.full(reseña, reseña.fk_user_reseña, reseña.fk_libro_reseña)
    
    @handle_errors
    @role_required(roles=["Usuario", "Admin"])
    def put(self, id):
        reseña = ReseñaService.get_by_id(id)
        current_user_id = get_jwt_identity()
        if int(current_user_id) != int(reseña.fk_idUser) and "Admin" not in get_jwt().get('rol', []):
            return {"message": "No tiene permiso para modificar la reseña de este usuario"}
        reseña = ReseñaService.update(id, request.get_json())
        return {"message": f"Reseña con ID {id} actualizada correctamente.", "reseña": ReseñaDTO.full(reseña, reseña.fk_user_reseña, reseña.fk_libro_reseña)}, 200
                
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
        filters = {
            "page": int(request.args.get("page", 1)),
            "per_page": int(request.args.get("per_page", 10)),
            "nroValoracion": request.args.get("nroValoracion"),
            "ordenValoracion": request.args.get("ordenValoracion"),
            "idUserPost": request.args.get("idUserPost"),
            "fechaReseña": request.args.get("fechaReseña"),
            "idLibro": request.args.get("idLibro"),
            "nombre_usuario": request.args.get("nombre_usuario"),
            "titulo_libro": request.args.get("titulo_libro"),
        }
        filters = {k: v for k, v in filters.items() if v is not None}
        result = ReseñaService.get_all(filters)
        return jsonify({
            'reseñas': [ReseñaDTO.full(r, r.fk_user_reseña, r.fk_libro_reseña) for r in result.items],
            'total': result.total,
            'pages': result.pages,
            'page': int(request.args.get("page", 1))
        })
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def post(self):
        reseña = ReseñaService.create(request.get_json())
        return {"message": "Reseña creada exitosamente.", "reseña": ReseñaDTO.full(reseña, reseña.fk_user_reseña, reseña.fk_libro_reseña)}, 201
    
if __name__ == '__main__':
    pass