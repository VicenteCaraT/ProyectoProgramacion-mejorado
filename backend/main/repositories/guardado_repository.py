from .. import db
from main.models import GuardadoModel
from .base_repository import BaseRepository

class GuardadoRepository(BaseRepository):
    model = GuardadoModel

    @classmethod
    def _apply_filters(cls, query, filters):
        if filters.get("idUsuario"):
            query = query.filter(GuardadoModel.fk_idUser == filters["idUsuario"])
        if filters.get("libro_id"):
            query = query.filter(GuardadoModel.fk_idLibro == filters["libro_id"])
        return query
