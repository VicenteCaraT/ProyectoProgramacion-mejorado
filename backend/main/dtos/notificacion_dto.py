from .usuario_dto import UsuarioDTO

class NotificacionDTO:
    @staticmethod
    def full(notificacion, usuario):
        return {
            "id": notificacion.idNotificacion,
            "usuario": UsuarioDTO.full(usuario),
            "descripcion": notificacion.descripcion
        }
