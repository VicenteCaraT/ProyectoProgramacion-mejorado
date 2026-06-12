from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import NotificacionModel
from main.auth.decorators import role_required, handle_errors

#implementar envio de mail

class Notificacion(Resource):
    
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def get(self, id):
        notificacion = db.session.query(NotificacionModel).get_or_404(id)
        return notificacion.to_json()

    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def delete(self, id):
        notificacion = db.session.query(NotificacionModel).get_or_404(id)
        db.session.delete(notificacion)
        db.session.commit()
        return '', 204

class Notificaciones(Resource):
    
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def get(self):
        page = 1

        per_page = 10

        notificaciones = db.session.query(NotificacionModel)

        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))

        ### FILTROS ###
        usuario = request.args.get('usuario')

        #usuario
        
        if usuario:
            notificaciones=notificaciones.filter(NotificacionModel.fk_idUser == usuario)

        ### FIN FILTROS ###

        # obtener valor paginado
        notificaciones = notificaciones.paginate(page=page, per_page=per_page, error_out=True)

        return jsonify({'notificaciones': [usuario.to_json() for usuario in notificaciones],
                    'total':notificaciones.total,
                    'pages':notificaciones.pages,
                    'page':page    
                        })

    @handle_errors
    @role_required(roles=["Admin"])
    def post(self):
        notificacion = NotificacionModel.from_json(request.get_json())
        db.session.add(notificacion)
        db.session.commit()
        from flask import current_app
        current_app.logger.info(f"Notificación creada: {notificacion}")
        return {
            "message": "Notificación creada exitosamente.",
            "notificacion": notificacion.to_json()
        }, 201


if __name__ == '__main__':
    pass