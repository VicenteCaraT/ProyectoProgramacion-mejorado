from main.repositories import NotificacionRepository, UsuarioRepository
from main.models import NotificacionModel
from .base_service import BaseService

class NotificacionService(BaseService):
    repository = NotificacionRepository
    model = NotificacionModel
    
    @classmethod
    def create(cls, data):
        user_id = data.get("usuario")
        if UsuarioRepository.get_by_id(user_id) is None:
            raise ValueError(f"El usuario ID {user_id} no existe")
        notificacion = cls.model.from_json(data)
        return cls.repository.save(notificacion)
