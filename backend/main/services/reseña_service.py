from main.repositories import ReseñaRepository, UsuarioRepository, LibroRepository
from main.models import ReseñaModel
from .base_service import BaseService

class ReseñaService(BaseService):
    repository = ReseñaRepository
    model = ReseñaModel
    
    @classmethod
    def create(cls, data):
        user_id = data.get("usuario")
        libro_id = data.get("libro")
        if UsuarioRepository.get_by_id(user_id) is None:
            raise ValueError(f"El usuario ID {user_id} no existe")
        if LibroRepository.get_by_id(libro_id) is None:
            raise ValueError(f"El libro ID {libro_id} no existe")
        reseña = cls.model.from_json(data)
        return cls.repository.save(reseña)