from .. import db
from main.models import UsuarioModel
from .base_repository import BaseRepository

class UsuarioRepository(BaseRepository):
    model = UsuarioModel

    @classmethod
    def get_by_email(cls, email):
        return db.session.query(UsuarioModel).filter_by(email=email).first()

    @classmethod
    def exists_by_email(cls, email):
        return db.session.query(UsuarioModel).filter_by(email=email).scalar() is not None

    @classmethod
    def _apply_filters(cls, query, filters):
        if filters.get("rol"):
            query = query.filter(UsuarioModel.rol.like(f"%{filters['rol']}%"))
        if filters.get("nombre"):
            query = query.filter(UsuarioModel.nombre.like(f"%{filters['nombre']}%"))
        if filters.get("dni"):
            query = query.filter(UsuarioModel.dni.like(f"%{filters['dni']}%"))
        if filters.get("telefono"):
            query = query.filter(UsuarioModel.telefono.like(f"%{filters['telefono']}%"))
        if filters.get("email"):
            query = query.filter(UsuarioModel.email.like(f"%{filters['email']}%"))
        if filters.get("estado"):
            query = query.filter(UsuarioModel.estado.like(f"%{filters['estado']}%"))
        return query
