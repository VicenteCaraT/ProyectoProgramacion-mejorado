from .. import db
from main.models import PrestamoModel, LibroModel, UsuarioModel
from sqlalchemy import func
from datetime import datetime
from .base_repository import BaseRepository

class PrestamoRepository(BaseRepository):
    model = PrestamoModel

    @classmethod
    def _apply_filters(cls, query, filters):
        if filters.get("idUsuario"):
            query = query.filter(PrestamoModel.fk_idUser == filters["idUsuario"])
        if filters.get("nombre_usuario"):
            query = query.join(UsuarioModel, PrestamoModel.fk_idUser == UsuarioModel.idUser).filter(
                func.lower(UsuarioModel.user).like(f"%{filters['nombre_usuario'].lower()}%")
            )
        if filters.get("inicio_prestamo"):
            fecha = datetime.strptime(filters["inicio_prestamo"], "%d-%m-%Y")
            query = query.filter(PrestamoModel.inicio_prestamo == fecha)
        if filters.get("fin_prestamo"):
            fecha = datetime.strptime(filters["fin_prestamo"], "%d-%m-%Y")
            query = query.filter(PrestamoModel.fin_prestamo == fecha)
        if filters.get("cant_libros"):
            query = query.outerjoin(PrestamoModel.fk_idLibro).group_by(
                PrestamoModel.idPrestamo
            ).having(func.count(LibroModel.idLibro) == int(filters["cant_libros"]))
        if filters.get("libro_id"):
            libro = LibroModel.query.get_or_404(filters["libro_id"])
            query = query.filter(PrestamoModel.fk_idLibro.contains(libro))
        if filters.get("titulo"):
            query = query.join(PrestamoModel.fk_idLibro).filter(
                func.lower(LibroModel.titulo).like(f"%{filters['titulo'].lower()}%")
            )
        if filters.get("estado"):
            query = query.filter(PrestamoModel.estado.like(f"%{filters['estado']}%"))
        return query
