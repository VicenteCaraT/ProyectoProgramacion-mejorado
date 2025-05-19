# from flask_restful import Resource
# from flask import request, jsonify
# from .. import db
# from main.models import UsuarioModel, LibroModel, GuardadoModel
# from main.auth.decorators import role_required
# from flask_jwt_extended import jwt_required

# class Guardado(Resource):
#     def get(self, id):
#         guardado = db.session.query(GuardadoModel).get_or_404(id)
#         return guardado.to_json()
    
#     def delete(self, id):
#         guardado = db.session.query(Guardado).get_or_404(id)
#         db.session.delete(guardado)
#         db.session.commit()
#         return '', 204
    
# class Guardados(Resource):
#     def get(self):
#         page = 1
        
#         per_page = 10
        
#         guardados = db.session.query(GuardadoModel)
        
#         if request.args.get('page'):
#             page = int(request.args.get('page'))
#         if request.args.get('per_page'):
#             per_page = int(request.args.get('per_page'))
            
#         ## FILTROS ##
#         usuario = request.args.get('idUsuario')
#         libro = request.args.get('libro_id')
        
#         #usuario
#         if usuario:
#             guardados = guardados.filter(GuardadoModel.fk_idUser == usuario)
            
#         #libro
#         if libro:
#             guardados = guardados.filte(GuardadoModel.fk_idLibro == libro)
        
        
#         guardados = guardados.paginate(page=page, per_page=per_page, error_out=True)
        
#         return jsonify({'guardados' : [guardado.to_json() for guardado in guardados],
#                     'total' : guardados.total,
#                     'pages': guardados.pages,
#                     'page' : page
#             })