from .usuario_dto import UsuarioDTO
from .libro_dto import LibroDTO

class GuardadoDTO:
    @staticmethod
    def full(guardado, usuario, libro):
        return {
            "id": guardado.idGuardado,
            "usuario": UsuarioDTO.full(usuario),
            "libro": LibroDTO.full(libro)
        }
