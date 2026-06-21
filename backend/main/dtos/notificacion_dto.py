from .usuario_dto import UsuarioDTO

class NotificacionDTO:
    @staticmethod
    def full(notificacion):
        return {
            "id": notificacion.idNotificacion,
            "usuario": UsuarioDTO.full(notificacion.fk_user_notificacion),
            "descripcion": notificacion.descripcion
        }
