from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import AutorModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from main.auth.decorators import role_required, handle_errors

class Autor(Resource):
    
    @handle_errors
    @jwt_required(optional=True)
    def get(self, id):
        autor = db.session.query(AutorModel).get_or_404(id)
        return {
            "message": "Autor obtenido exitosamente",
            "autor": autor.to_json()
        }, 200
    
    @handle_errors
    @role_required(roles=['Admin'])
    def put(self, id):
        autor = db.session.query(AutorModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(autor, key, value)
        db.session.add(autor)
        db.session.commit()
        return {
            "message": "Autor actualizado correctamente",
            "autor": autor.to_json()
        }, 200

    
    @handle_errors
    @role_required(roles=['Admin'])
    def delete(self, id):
        autor = db.session.query(AutorModel).get_or_404(id)
        db.session.delete(autor)
        db.session.commit()
        return '', 204

class Autores(Resource):

    @handle_errors
    @jwt_required(optional=True)
    def get(self):
        autores = db.session.query(AutorModel).all()
        return {
            "message": "Lista de autores obtenida",
            "autores": [autor.to_json() for autor in autores]
        }, 200
        
    @handle_errors
    @role_required(roles=["Admin"])
    def post(self):
        autor = AutorModel.from_json(request.get_json())
        db.session.add(autor)
        db.session.commit()
        return {
            "message": "Autor creado exitosamente",
            "autor": autor.to_json()
        }, 201
    
if __name__ == '__main__':
    pass