class LibroDTO:
    @staticmethod
    def full(libro):
        total_reseñas = len(libro.reseñas_libro)
        promedio = 0
        if total_reseñas > 0:
            promedio = sum(
                float(r.valoracion.split('/')[0]) for r in libro.reseñas_libro
            ) / total_reseñas
        return {
            "id": libro.idLibro,
            "img": libro.book_img,
            "titulo": libro.titulo,
            "cantidad": libro.cantidad,
            "autor": [a.to_json() for a in libro.fk_idAutor],
            "editorial": libro.editorial,
            "genero": libro.genero,
            "sinopsis": libro.sinopsis,
            "total_reseñas": total_reseñas,
            "promedio_valoracion": round(promedio, 2)
        }

    @staticmethod
    def short(libro):
        return {
            "id": libro.idLibro,
            "img": libro.book_img,
            "titulo": libro.titulo,
            "autor": [a.to_json_short() for a in libro.fk_idAutor],
            "editorial": libro.editorial,
            "genero": libro.genero,
            "sinopsis": libro.sinopsis
        }
