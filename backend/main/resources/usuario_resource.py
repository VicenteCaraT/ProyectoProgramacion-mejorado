from flask_restful import Resource
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from main.auth.decorators import role_required, handle_errors
from main.services import UsuarioService
from main.dtos import UsuarioDTO
from .helpers import paginated_response


class Usuario(Resource):
    
    @handle_errors
    @jwt_required(optional=True)
    def get(self, id):
        current_identity = get_jwt_identity()
        usuario = UsuarioService.get_by_id(id)
        if int(current_identity) != int(id):
            return UsuarioDTO.short(usuario)
        return UsuarioDTO.full(usuario)
    
    @handle_errors
    @role_required(roles = ["Admin", "Usuario"])
    def put(self, id): 
        current_user_id = get_jwt_identity()
        if int(current_user_id) != int(id) and "Admin" not in get_jwt().get('rol', []):
            return {"message": "No tienes permiso para modificar este perfil"}, 403
        usuario = UsuarioService.update(id, request.get_json())
        return {"message": f"Usuario con ID {id} actualizado correctamente.", "usuario": UsuarioDTO.full(usuario)}, 200
    
    @handle_errors
    @role_required(roles = ["Admin", "Usuario"])
    def delete(self, id):
        current_user_id = get_jwt_identity()
        usuario = UsuarioService.get_by_id(id)
        if int(current_user_id) != int(usuario.idUser) and "Admin" not in get_jwt().get('rol', []):
            return {"message": "Notiene permisos para borrar este perfil"}, 403
        UsuarioService.delete(id)
        return '', 204

class Usuarios(Resource):
    
    @handle_errors
    @jwt_required(optional=True)
    def get(self):
        return paginated_response(UsuarioService, UsuarioDTO, 'usuarios',
            rol="rol", nombre="nombre", dni="dni",
            telefono="telefono", email="email", estado="estado")
        
    @handle_errors
    def post(self):
        usuario = UsuarioService.create(request.get_json())
        return {"message": "Usuario creado exitosamente", "usuario": UsuarioDTO.full(usuario)}, 201
    
if __name__ == '__main__':
    pass