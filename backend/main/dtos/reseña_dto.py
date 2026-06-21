from .usuario_dto import UsuarioDTO
from .libro_dto import LibroDTO

class ReseñaDTO:
    @staticmethod
    def full(reseña):
        return {
            "id": reseña.idReseña,
            "usuario": UsuarioDTO.full(reseña.fk_user_reseña),
            "libro": LibroDTO.full(reseña.fk_libro_reseña),
            "fecha": reseña.fecha.strftime("%d-%m-%Y"),
            "descripcion": reseña.descripcion,
            "valoracion": reseña.valoracion
        }
