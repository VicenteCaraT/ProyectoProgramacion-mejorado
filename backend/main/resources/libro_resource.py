from flask_restful import Resource
from flask import request, jsonify
from main.auth.decorators import role_required, handle_errors
from main.services import LibroService
from main.dtos import LibroDTO


class Libro(Resource):
    
    @handle_errors
    def get(self, id):
        libro = LibroService.get_by_id(id)
        return LibroDTO.full(libro)
    
    @handle_errors
    @role_required(roles=["Admin"])
    def put(self, id):
        libro = LibroService.update (id, request.get_json())
        return {"message": "Libro actualizado correctamente", "libro": LibroDTO.full(libro)}, 200

    @handle_errors
    @role_required(roles=["Admin"])
    def delete(self, id):
        LibroService.delete(id)
        return '', 204

class Libros(Resource):
    
    @handle_errors
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        filters = {
            "page": page,
            "per_page": per_page,
            "genero": request.args.get("genero"),
            "autor": request.args.get("autor"),
            "titulo": request.args.get("titulo"),
            "editorial": request.args.get("editorial"),
            "orden": request.args.get("orden"),
            "sin_stock": request.args.get("sin_stock"),
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        from main.repositories import LibroRepository
        from main.models import LibroModel
        from sqlalchemy import func
        result = LibroRepository.get_all(page=page, per_page=per_page, filters=filters)

        if request.args.get("orden") == "ranking":
            libros_list = list(result.items)
            libros_list.sort(
                key=lambda libro: (
                    sum(float(r.valoracion.split('/')[0]) for r in libro.reseñas_libro) / len(libro.reseñas_libro)
                    if libro.reseñas_libro else 0
                ),
                reverse=True
            )
            total = len(libros_list)
            pages = (total + per_page - 1) // per_page
            libros_paginados = libros_list[(page - 1) * per_page : page * per_page]
            return jsonify({
                'libros': [LibroDTO.full(l) for l in libros_paginados],
                'total': total,
                'pages': pages,
                'page': page
            })

        return jsonify({
            'libros': [LibroDTO.full(l) for l in result.items],
            'total': result.total,
            'pages': result.pages,
            'page': page
        })
    
    @handle_errors
    @role_required(roles=["Admin"])
    def post(self):
        libro = LibroService.create(request.get_json())
        return {"message": "Libro creado exitosamente", "libro": LibroDTO.full(libro)}, 201
        
if __name__ == '__main__':
    pass
