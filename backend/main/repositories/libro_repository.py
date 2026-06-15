from .. import db
from main.models import LibroModel, AutorModel
from sqlalchemy import func
from .base_repository import BaseRepository

class LibroRepository(BaseRepository):
    model = LibroModel
    
    @classmethod
    def _apply_filters(cls, query, filters):
        if filters.get("genero"):
            query = query.filter(LibroModel.genero.like(f"%{filters['genero']}%"))
        if filters.get("titulo"):
            query = query.filter(LibroModel.titulo.like(f"%{filters['titulo']}%"))
        if filters.get("editorial"):
            query = query.filter(LibroModel.editorial.like(f"%{filters['editorial']}%"))
        if filters.get("autor"):
            autor_lower = filters['autor'].lower()
            query = query.join(LibroModel.fk_idAutor).filter(
                func.lower(AutorModel.nombre).like(f"%{autor_lower}%") |
                func.lower(AutorModel.apellido).like(f"%{autor_lower}%") |
                func.lower(AutorModel.apodo).like(f"%{autor_lower}%")
            )
        return query
    