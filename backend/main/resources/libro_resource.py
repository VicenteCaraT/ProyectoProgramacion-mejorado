from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import LibroModel, AutorModel
from sqlalchemy import func, desc
from main.auth.decorators import role_required, handle_errors
from flask_jwt_extended import jwt_required

#LIBROS = {
#    1:{'Titulo':'Odisea', 'Autor': 'Homero', 'Genero':'Poema epico', 'Editorial':'La Estacion'},
#    2:{'Titulo':'Don Quijote de la Mancha', 'Autor':'Miguel de Cervantes', 'Genero': 'Aventura', 'Editorial': 'Urbano Manini'},
#    3:{'Titulo':'El Código Da Vinci', 'Autor':'Dan Brown', 'Genero':'Novela Policiaca/Ficción', 'Editorial':'Doubleday'}
#}

class Libro(Resource):
    
    # Cambiado el jwt ya que un usuario sin rol puede ingresar al home
    #@jwt_required(optional=True)
    @handle_errors
    def get(self, id):
        libro = db.session.query(LibroModel).get_or_404(id)
        return libro.to_json()
    
    @handle_errors
    @role_required(roles=["Admin"])
    def put(self, id):
        libro = db.session.query(LibroModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            if key == 'autor':
                nuevo_autor_id = value
                nuevo_autor = AutorModel.query.get_or_404(nuevo_autor_id)
                libro.fk_idAutor = [nuevo_autor]
            else:
                setattr(libro, key, value)
        db.session.add(libro)
        db.session.commit()
        return {
            "message": "Libro actualizado correctamente.",
            "libro": libro.to_json()
        }, 200

    @handle_errors
    @role_required(roles=["Admin"])
    def delete(self, id):
        libro = db.session.query(LibroModel).get_or_404(id)
        db.session.delete(libro)
        db.session.commit()
        return '', 204

class Libros(Resource):
    
    @handle_errors
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        libros_query = db.session.query(LibroModel)

        ### FILTROS ###
        genero = request.args.get("genero")
        autor = request.args.get("autor")
        titulo = request.args.get("titulo")
        editorial = request.args.get("editorial")
        orden = request.args.get("orden")
        sin_stock = request.args.get("sin_stock")
        
        # Filtros de búsqueda
        if genero:
            libros_query = libros_query.filter(LibroModel.genero.like(f"%{genero}%"))
        if autor:
            autor_lower = autor.lower()
            libros_query = libros_query.join(LibroModel.fk_idAutor).filter(
                func.lower(AutorModel.nombre).like(f"%{autor_lower}%") |
                func.lower(AutorModel.apellido).like(f"%{autor_lower}%") |
                func.lower(AutorModel.apodo).like(f"%{autor_lower}%")
            )
        if titulo:
            libros_query = libros_query.filter(LibroModel.titulo.like(f"%{titulo}%"))
        if editorial:
            libros_query = libros_query.filter(LibroModel.editorial.like(f"%{editorial}%"))
        if sin_stock == "true":
            libros_query = libros_query.filter(LibroModel.cantidad == 0)
        if orden == "mayor_stock":
            libros_query = libros_query.order_by(LibroModel.cantidad.desc())

        # Ordenar por ranking dinámico (promedio_valoracion)
        libros = libros_query.all()
        if orden == "ranking":
            libros.sort(
                key=lambda libro: (
                    sum([float(r.valoracion.split('/')[0]) for r in libro.reseñas_libro]) / len(libro.reseñas_libro)
                    if libro.reseñas_libro else 0
                ),
                reverse=True
            )
            
        # Paginado manual
        total = len(libros)
        pages = (total + per_page - 1) // per_page
        libros_paginados = libros[(page - 1) * per_page : page * per_page]

        return jsonify({
            'libros': [libro.to_json() for libro in libros_paginados],
            'total': total,
            'pages': pages,
            'page': page
        })
    
    @handle_errors
    @role_required(roles=["Admin"])
    def post(self):
        data = request.get_json()
        autor_exist = data.get("autor")
        libro = LibroModel.from_json(data)

        if autor_exist:
            if not isinstance(autor_exist, list):
                autor_exist = [autor_exist]
            autores = AutorModel.query.filter(AutorModel.idAutor.in_(autor_exist)).all()
            libro.fk_idAutor.extend(autores)
        db.session.add(libro)
        db.session.commit()
        return {
            "message": "Libro creado exitosamente.",
            "libro": libro.to_json()
        }, 201
        
if __name__ == '__main__':
    pass
