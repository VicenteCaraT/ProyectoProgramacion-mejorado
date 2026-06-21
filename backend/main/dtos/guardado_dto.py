from .usuario_dto import UsuarioDTO
from .libro_dto import LibroDTO

class GuardadoDTO:
    @staticmethod
    def full(guardado):
        return {
            "id": guardado.idGuardado,
            "usuario": UsuarioDTO.full(guardado.fk_user_guardado),
            "libro": LibroDTO.full(guardado.fk_libro_guardado)
        }
