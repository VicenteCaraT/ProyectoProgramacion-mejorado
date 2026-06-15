from main.repositories import NotificacionRepository, UsuarioRepository
from main.models import NotificacionModel

class NotificacionService:
    @staticmethod
    def get_by_id(id):
        return NotificacionRepository.get_by_id(id)

    @staticmethod
    def get_all(filters):
        return NotificacionRepository.get_all(
            page=filters.pop("page", 1),
            per_page=filters.pop("per_page", 10),
            filters=filters
        )

    @staticmethod
    def create(data):
        user_id = data.get("usuario")
        if UsuarioRepository.get_by_id(user_id) is None:
            raise ValueError(f"El usuario ID {user_id} no existe")
        notificacion = NotificacionModel.from_json(data)
        return NotificacionRepository.save(notificacion)

    @staticmethod
    def delete(id):
        notificacion = NotificacionRepository.get_by_id(id)
        NotificacionRepository.delete(notificacion)
