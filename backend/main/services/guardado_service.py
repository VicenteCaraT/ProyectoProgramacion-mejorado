from main.repositories import GuardadoRepository, UsuarioRepository, LibroRepository
from main.models import GuardadoModel
from .base_service import BaseService

class GuardadoService(BaseService):
    repository = GuardadoRepository
    model = GuardadoModel

    @classmethod
    def create(cls, user_id, libro_id):
        if UsuarioRepository.get_by_id(user_id) is None:
            raise ValueError(f"El usuario ID {user_id} no existe")
        if LibroRepository.get_by_id(libro_id) is None:
            raise ValueError(f"El libro ID {libro_id} no existe")
        existente = GuardadoRepository.get_all(filters={
            "idUsuario": user_id, "libro_id": libro_id
        })
        if existente.total > 0:
            raise ValueError("Este libro ya fue guardado por el usuario actual")
        guardado = GuardadoModel(fk_idUser=user_id, fk_idLibro=libro_id)
        return cls.repository.save(guardado)
