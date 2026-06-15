from flask_restful import Resource
from flask import request, jsonify
from main.auth.decorators import role_required, handle_errors
from main.services import NotificacionService
from main.dtos import NotificacionDTO

#implementar envio de mail

class Notificacion(Resource):
    
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def get(self, id):
        notificacion = NotificacionService.get_by_id(id)
        return NotificacionDTO.full(notificacion, notificacion.fk_user_notificacion)

    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def delete(self, id):
        NotificacionService.delete(id)
        return '', 204

class Notificaciones(Resource):
    
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def get(self):
        filters = {
            "page": int(request.args.get("page", 1)),
            "per_page": int(request.args.get("per_page", 10)),
            "usuario": request.args.get("usuario"),
        }
        filters = {k: v for k, v in filters.items() if v is not None}
        result = NotificacionService.get_all(filters)
        return jsonify({
            'notificaciones': [NotificacionDTO.full(n, n.fk_user_notificacion) for n in result.items],
            'total': result.total,
            'pages': result.pages,
            'page': int(request.args.get("page", 1))
        })
        
    @handle_errors
    @role_required(roles=["Admin"])
    def post(self):
        notificacion = NotificacionService.create(request.get_json())
        return {
            "message": "Notificacion creada exitosamente.", 
            "notificacion": NotificacionDTO.full(notificacion, notificacion.fk_user_notificacion)
        }, 201


if __name__ == '__main__':
    pass