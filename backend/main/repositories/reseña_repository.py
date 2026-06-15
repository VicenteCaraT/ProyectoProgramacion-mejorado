from .. import db
from main.models import ReseñaModel, UsuarioModel, LibroModel
from sqlalchemy import desc, asc, func
from datetime import datetime
from .base_repository import BaseRepository

class ReseñaRepository(BaseRepository):
    model = ReseñaModel

    @classmethod
    def _apply_filters(cls, query, filters):
        if filters.get("nroValoracion"):
            query = query.filter(
                ReseñaModel.valoracion.like(f"%{filters['nroValoracion']}%")
            )
        if filters.get("ordenValoracion") == "Valoraciones_desc":
            query = query.order_by(desc(ReseñaModel.valoracion))
        elif filters.get("ordenValoracion") == "Valoraciones_asc":
            query = query.order_by(asc(ReseñaModel.valoracion))
        if filters.get("idUserPost"):
            query = query.filter(ReseñaModel.fk_idUser == filters["idUserPost"])
        if filters.get("fechaReseña"):
            fecha = datetime.strptime(filters["fechaReseña"], "%d-%m-%Y")
            query = query.filter(ReseñaModel.fecha == fecha)
        if filters.get("idLibro"):
            query = query.filter(ReseñaModel.fk_idLibro == filters["idLibro"])
        if filters.get("titulo_libro"):
            query = query.join(ReseñaModel.fk_libro_reseña).filter(
                func.lower(LibroModel.titulo).like(f"%{filters['titulo_libro'].lower()}%")
            )
        if filters.get("nombre_usuario"):
            query = query.join(UsuarioModel, ReseñaModel.fk_idUser == UsuarioModel.idUser).filter(
                func.lower(UsuarioModel.user).like(f"%{filters['nombre_usuario'].lower()}%")
            )
        return query
