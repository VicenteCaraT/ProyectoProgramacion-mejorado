from .usuario_dto import UsuarioDTO
from .libro_dto import LibroDTO

class PrestamoDTO:
    @staticmethod
    def full(prestamo, usuario, libros):
        return {
            "id": prestamo.idPrestamo,
            "usuario": UsuarioDTO.full(usuario),
            "libro": [LibroDTO.full(l) for l in libros],
            "inicio_prestamo": prestamo.inicio_prestamo.strftime("%d-%m-%Y"),
            "fin_prestamo": prestamo.fin_prestamo.strftime("%d-%m-%Y"),
            "estado": prestamo.estado
        }
