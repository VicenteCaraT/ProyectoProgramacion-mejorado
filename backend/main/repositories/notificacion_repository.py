from .. import db
from main.models import NotificacionModel
from .base_repository import BaseRepository

class NotificacionRepository(BaseRepository):
    model = NotificacionModel

    @classmethod
    def _apply_filters(cls, query, filters):
        if filters.get("usuario"):
            query = query.filter(NotificacionModel.fk_idUser == filters["usuario"])
        return query
