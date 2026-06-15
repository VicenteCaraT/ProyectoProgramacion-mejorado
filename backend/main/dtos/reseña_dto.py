from .usuario_dto import UsuarioDTO
from .libro_dto import LibroDTO

class ReseñaDTO:
    @staticmethod
    def full(reseña, usuario, libro):
        return {
            "id": reseña.idReseña,
            "usuario": UsuarioDTO.full(usuario),
            "libro": LibroDTO.full(libro),
            "fecha": reseña.fecha.strftime("%d-%m-%Y"),
            "descripcion": reseña.descripcion,
            "valoracion": reseña.valoracion
        }
