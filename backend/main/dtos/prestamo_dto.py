from .usuario_dto import UsuarioDTO
from .libro_dto import LibroDTO

class PrestamoDTO:
    @staticmethod
    def full(prestamo):
        return {
            "id": prestamo.idPrestamo,
            "usuario": UsuarioDTO.full(prestamo.fk_user_prestamo),
            "libro": [LibroDTO.full(l) for l in prestamo.fk_idLibro],
            "inicio_prestamo": prestamo.inicio_prestamo.strftime("%d-%m-%Y"),
            "fin_prestamo": prestamo.fin_prestamo.strftime("%d-%m-%Y"),
            "estado": prestamo.estado
        }
