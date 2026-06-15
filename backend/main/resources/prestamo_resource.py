from flask_restful import Resource
from flask import request, jsonify
from datetime import datetime, timedelta
from main.auth.decorators import role_required, handle_errors
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from main.services import PrestamoService
from main.dtos import PrestamoDTO

#implementar envio de mail

class Prestamo(Resource):
    
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    # solo el usuario puede ver los prestamos de uno mismo
    # el admin y bibliotecario puede ver cualquiera
    def get(self, id):
        prestamo = PrestamoService.get_by_id(id)
        return PrestamoDTO.full(prestamo, prestamo.fk_user_prestamo, prestamo.fk_idLibro)

    @handle_errors
    @role_required(roles=["Admin"])
    def put(self, id):
        prestamo = PrestamoService.update(id, request.get_json())
        return{"message": "Préstamo actualizado correctamente.", "prestamo": PrestamoDTO.full(prestamo, prestamo.fk_user_prestamo, prestamo.fk_idLibro)}, 200
    
    @handle_errors
    @role_required(roles=["Admin"])
    def delete(self, id):
        PrestamoService.delete(id)
        return {"message": "Prástamo eliminado y libros devueltos al stock"}, 200
    
class Prestamos(Resource):
    
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def get(self):
        filters = {
            "page": int(request.args.get("page", 1)),
            "per_page": int(request.args.get("per_page", 10)),
            "idUsuario": request.args.get("idUsuario"),
            "inicio_prestamo": request.args.get("inicio_prestamo"),
            "fin_prestamo": request.args.get("fin_prestamo"),
            "cant_libros": request.args.get("cant_libros"),
            "libro_id": request.args.get("libro_id"),
            "titulo": request.args.get("titulo"),
            "estado": request.args.get("estado"),
            "nombre_usuario": request.args.get("nombre_usuario"),
        }
        filters = {k: v for k, v in filters.items() if v is not None}
        result = PrestamoService.get_all(filters)
        return jsonify({
            'prestamos': [PrestamoDTO.full(p, p.fk_user_prestamo, p.fk_idLibro) for p in result.items],
            'total': result.total,
            'pages': result.pages,
            'page': int(request.args.get("page", 1))
        })
        
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def post(self):
        prestamo = PrestamoService.create(request.get_json())
        return {"message": "Préstamo creado exitosamente.", "prestamo": PrestamoDTO.full(prestamo, prestamo.fk_user_prestamo, prestamo.fk_idLibro)}, 201
        
    @handle_errors
    @role_required(roles=["Admin"])
    def patch(self):
        cambios = PrestamoService.expire_overdue()
        return {"message": f"{cambios} préstamos vencidos fueron marcados como 'Terminados'."}, 200
        
if __name__ == '__main__':
    pass