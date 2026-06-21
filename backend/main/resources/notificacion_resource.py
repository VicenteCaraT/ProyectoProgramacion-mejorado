from flask_restful import Resource
from flask import request, jsonify
from main.auth.decorators import role_required, handle_errors
from main.services import NotificacionService
from main.dtos import NotificacionDTO
from .helpers import paginated_response


class Notificacion(Resource):
    
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def get(self, id):
        notificacion = NotificacionService.get_by_id(id)
        return NotificacionDTO.full(notificacion)

    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def delete(self, id):
        NotificacionService.delete(id)
        return '', 204

class Notificaciones(Resource):
    
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def get(self):
        return paginated_response(NotificacionService, NotificacionDTO, 'notificaciones',
            usuario="usuario")
        
    @handle_errors
    @role_required(roles=["Admin"])
    def post(self):
        notificacion = NotificacionService.create(request.get_json())
        return {
            "message": "Notificacion creada exitosamente.", 
            "notificacion": NotificacionDTO.full(notificacion)
        }, 201


if __name__ == '__main__':
    pass