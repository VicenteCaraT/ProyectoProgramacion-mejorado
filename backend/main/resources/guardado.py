from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel, LibroModel, GuardadoModel
from main.auth.decorators import role_required, handle_errors
from flask_jwt_extended import jwt_required, get_jwt_identity

class Guardado(Resource):
    
    @handle_errors
    @jwt_required()
    def get(self, id):
        guardado = db.session.query(GuardadoModel).get_or_404(id)
        return guardado.to_json()
    
    @handle_errors
    @jwt_required()
    def delete(self, id):
        guardado = db.session.query(GuardadoModel).get_or_404(id)
        db.session.delete(guardado)
        db.session.commit()
        return '', 204
    
class Guardados(Resource):
    
    @handle_errors
    @jwt_required()
    def get(self):
        page = 1
        
        per_page = 10
        
        guardados = db.session.query(GuardadoModel)
        
        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))
            
        ## FILTROS ##
        usuario = request.args.get('idUsuario')
        libro = request.args.get('libro_id')
        
        #usuario
        if usuario:
            guardados = guardados.filter(GuardadoModel.fk_idUser == usuario)
            
        #libro
        if libro:
            guardados = guardados.filter(GuardadoModel.fk_idLibro == libro)
        
        
        guardados = guardados.paginate(page=page, per_page=per_page, error_out=True)
        
        return jsonify({'guardados' : [guardado.to_json() for guardado in guardados],
                    'total' : guardados.total,
                    'pages': guardados.pages,
                    'page' : page
            })
    
    @handle_errors
    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user_id = get_jwt_identity()
        libro_id = data.get("libro")

        if not libro_id:
            return {"message": "Falta el ID del libro."}, 400

        # Verificar si ya está guardado por el mismo usuario
        existente = GuardadoModel.query.filter_by(
            fk_idUser=current_user_id,
            fk_idLibro=libro_id
        ).first()

        if existente:
            return {"message": "Este libro ya fue guardado por el usuario actual."}, 409

        nuevo_guardado = GuardadoModel(
            fk_idUser=current_user_id,
            fk_idLibro=libro_id
        )
        db.session.add(nuevo_guardado)
        db.session.commit()

        return {
            "message": "Libro guardado exitosamente.",
            "guardado": nuevo_guardado.to_json()
        }, 201