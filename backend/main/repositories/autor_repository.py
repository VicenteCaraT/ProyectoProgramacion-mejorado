from .. import db
from main.models import AutorModel
from .base_repository import BaseRepository

class AutorRepository(BaseRepository):
    model = AutorModel

    @classmethod
    def _apply_filters(cls, query, filters):
        if filters.get("nombre"):
            query = query.filter(AutorModel.nombre.like(f"%{filters['nombre']}%"))
        if filters.get("apellido"):
            query = query.filter(AutorModel.apellido.like(f"%{filters['apellido']}%"))
        if filters.get("apodo"):
            query = query.filter(AutorModel.apodo.like(f"%{filters['apodo']}%"))
        return query
