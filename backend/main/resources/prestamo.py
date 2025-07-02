from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import PrestamoModel, LibroModel, UsuarioModel
import re
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from main.auth.decorators import role_required, handle_errors
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required

#PRESTAMOS = {
#    1: {'usuario': 'usuario1', 'fechaI': '20/10/20', 'fechaT': '27/10/20' },
#    2: {'usuario': 'usuario2', 'fechaI': '21/10/20', 'fechaT': '28/10/20' },
#}

#implementar envio de mail

class Prestamo(Resource):
    
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    # solo el usuario puede ver los prestamos de uno mismo
    # el admin y bibliotecario puede ver cualquiera
    def get(self, id):
        prestamo = db.session.query(PrestamoModel).get_or_404(id)
        return prestamo.to_json()

    @handle_errors
    @role_required(roles=["Admin"])
    def put(self, id):
        
        prestamo = db.session.query(PrestamoModel).get_or_404(id)

        data = request.get_json()

        # Fechas
        if "inicio_prestamo" in data:
            try:
                prestamo.inicio_prestamo = datetime.strptime(data["inicio_prestamo"], "%d-%m-%Y")
            except ValueError:
                return {"message": "Formato de fecha inválido en 'inicio_prestamo', se espera dd-mm-aaaa"}, 400

        if "fin_prestamo" in data:
            try:
                prestamo.fin_prestamo = datetime.strptime(data["fin_prestamo"], "%d-%m-%Y")
            except ValueError:
                return {"message": "Formato de fecha inválido en 'fin_prestamo', se espera dd-mm-aaaa"}, 400

        # Estado
        estado_anterior = prestamo.estado
        nuevo_estado = data.get("estado")

        if nuevo_estado:
            prestamo.estado = nuevo_estado

            if nuevo_estado == "Activo" and estado_anterior != "Activo":
                for libro in prestamo.fk_idLibro:
                    if libro.cantidad > 0:
                        libro.cantidad -= 1
                    else:
                        return {"message": f"No hay cantidad disponible para el libro ID {libro.idLibro}"}, 400

            elif nuevo_estado == "Desactivado" and estado_anterior == "Activo":
                for libro in prestamo.fk_idLibro:
                    libro.cantidad += 1

        # Cambiar libro
        if "libro" in data:
            ids_libros = data["libro"]            
            if isinstance(ids_libros, int):
                ids_libros = [ids_libros]
        
            if not isinstance(ids_libros, list):
                return {"message": "El campo 'libro' debe ser una lista de IDs"}, 400

            nuevos_libros = db.session.query(LibroModel).filter(LibroModel.idLibro.in_(ids_libros)).all()

            if len(nuevos_libros) != len(ids_libros):
                return {"message": "Uno o más libros no existen"}, 400

            prestamo.fk_idLibro = nuevos_libros
        db.session.commit()

        resultado = prestamo.to_json()
        return {
            "message": "Préstamo actualizado correctamente.",
            "prestamo": resultado
        }, 200
    
    @handle_errors
    @role_required(roles=["Admin"])
    def delete(self, id):
        prestamo = db.session.query(PrestamoModel).get_or_404(id)
        db.session.delete(prestamo)
        db.session.commit()
        return '', 204
    
class Prestamos(Resource):
    
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def get(self):
        page = 1
        per_page = 10

        prestamos = db.session.query(PrestamoModel)

        if request.args.get('page'):
            page = int(request.args.get('page'))
        if request.args.get('per_page'):
            per_page = int(request.args.get('per_page'))

        ### FILTROS ###

        usuario = request.args.get('idUsuario')
        fecha_inicio = request.args.get('inicio_prestamo')
        fecha_termino = request.args.get('fin_prestamo')
        cant_libros = request.args.get('cant_libros')
        libro = request.args.get('libro_id')
        cant_prestamo = request.args.get("cant_prestamos")
        estado = request.args.get('estado')

        #usuario
        if usuario:
            prestamos = prestamos.filter(PrestamoModel.fk_idUser == usuario)

        #inicio_prestamo
        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, '%d-%m-%Y')
            prestamos = prestamos.filter(PrestamoModel.inicio_prestamo == fecha_inicio)

        #fin_prestamo
        if fecha_termino:
            fecha_termino = datetime.strptime(fecha_termino, '%d-%m-%Y')
            prestamos = prestamos.filter(PrestamoModel.fin_prestamo == fecha_termino)
        
        #prestamos por cantidad de libros
        if cant_libros:
            prestamos = prestamos.outerjoin(PrestamoModel.fk_idLibro).group_by(PrestamoModel.idPrestamo).having(func.count(LibroModel.idLibro) == int(cant_libros))

        #Prestamo por libro especifico
        if libro:
            libro_id = LibroModel.query.get_or_404(libro)
            prestamos = prestamos.filter(PrestamoModel.fk_idLibro.contains(libro_id))
        
        #Ordenar de manera desc los usuarios con mas prestamos a los menos (Fixing)
        if cant_prestamo == "Desc_Prestamos":
            prestamos = prestamos.outerjoin(PrestamoModel.fk_user_prestamo).group_by(UsuarioModel.idUser).order_by(func.count().desc())
            
        # Filtro por estado
        if estado:
            prestamos = prestamos.filter(PrestamoModel.estado.like(f"%{estado}%"))
            
        # Ordenar por fecha de finalización más próxima
        if request.args.get('orden') == 'proximos':
            prestamos = prestamos.filter(PrestamoModel.estado == "Activo")
            prestamos = prestamos.order_by(PrestamoModel.fin_prestamo.asc())

        ### FIN FILTROS ###
        
        prestamos = prestamos.paginate(page=page, per_page=per_page, error_out=True)

        return jsonify({
            'prestamos': [prestamo.to_json() for prestamo in prestamos],
            'total': prestamos.total,
            'pages': prestamos.pages,
            'page': page
        })
    @handle_errors
    @role_required(roles=["Admin", "Usuario"])
    def post(self):
        data = request.get_json()
        user_id = data.get("usuario")
        libro_ids = data.get("libro")

        if not isinstance(libro_ids, list):
            libro_ids = [libro_ids]

        libros = LibroModel.query.filter(LibroModel.idLibro.in_(libro_ids)).all()
        if not libros:
            return {'message': 'Libro no encontrado'}, 404

        for libro in libros:
            if libro.cantidad <= 0:
                return {'message': f'Sin stock para el libro ID {libro.idLibro}'}, 400

            prestamo_existente = PrestamoModel.query \
                .filter(PrestamoModel.fk_idUser == user_id) \
                .filter(PrestamoModel.fk_idLibro.contains(libro)) \
                .filter(PrestamoModel.estado == "Activo") \
                .first()
            if prestamo_existente:
                return {'message': f'Ya existe un préstamo activo del libro ID {libro.idLibro} para el usuario'}, 400

        # formato "dd-mm-aaaa"
        if "inicio_prestamo" not in data or "fin_prestamo" not in data:
            hoy = datetime.today()
            data["inicio_prestamo"] = hoy.strftime("%d-%m-%Y")
            data["fin_prestamo"] = (hoy + timedelta(days=30)).strftime("%d-%m-%Y")

        prestamo = PrestamoModel.from_json(data)
        prestamo.estado = "Pendiente"

        for libro in libros:
            prestamo.fk_idLibro.append(libro)

        db.session.add(prestamo)
        db.session.commit()

        return {
            "message": "Préstamo creado exitosamente.",
            "prestamo": prestamo.to_json()
        }, 201
        
    @handle_errors
    @role_required(roles=["Admin"])
    def patch(self):
        hoy = datetime.today()

        prestamos = PrestamoModel.query.filter(PrestamoModel.estado == "Activo").all()
        cambios = 0

        for prestamo in prestamos:
            if prestamo.fin_prestamo < hoy:
                prestamo.estado = "Terminado"
                for libro in prestamo.fk_idLibro:
                    libro.cantidad += 1
                cambios += 1

        db.session.commit()
        return {
            "message": f"{cambios} préstamos vencidos fueron marcados como 'Terminado'."
        }, 200
        
if __name__ == '__main__':
    pass