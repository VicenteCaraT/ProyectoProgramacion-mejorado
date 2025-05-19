from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel, LibroModel, GuardadoModel
from main.auth.decorators import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity

class Guardado(Resource):
    
    @jwt_required()
    def get(self, id):
        guardado = db.session.query(GuardadoModel).get_or_404(id)
        return guardado.to_json()
    
    @jwt_required()
    def delete(self, id):
        guardado = db.session.query(GuardadoModel).get_or_404(id)
        db.session.delete(guardado)
        db.session.commit()
        return '', 204
    
class Guardados(Resource):
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
            guardados = guardados.filte(GuardadoModel.fk_idLibro == libro)
        
        
        guardados = guardados.paginate(page=page, per_page=per_page, error_out=True)
        
        return jsonify({'guardados' : [guardado.to_json() for guardado in guardados],
                    'total' : guardados.total,
                    'pages': guardados.pages,
                    'page' : page
            })
        
    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Verificar si el libro ya ha sido guardado anteriormente
        existente = GuardadoModel.query.filter_by(
            fk_idUser=current_user_id,
            fk_idLibro=data.get("libro")
        ).first()
        
        if existente:
            return {"message": "El libro ya fue guardado previamente."}, 409
        
        nuevo_guardado = GuardadoModel(
            fk_idUser=current_user_id,
            fk_idLibro=data.get("libro")
        )
        db.session.add(nuevo_guardado)
        db.session.commit()
        
        return nuevo_guardado.to_json(), 201