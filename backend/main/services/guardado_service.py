from main.repositories import GuardadoRepository
from main.models import GuardadoModel

class GuardadoService:
    @staticmethod
    def get_by_id(id):
        return GuardadoRepository.get_by_id(id)

    @staticmethod
    def get_all(filters):
        return GuardadoRepository.get_all(
            page=filters.pop("page", 1),
            per_page=filters.pop("per_page", 10),
            filters=filters
        )

    @staticmethod
    def create(user_id, libro_id):
        existente = GuardadoRepository.get_all(filters={
            "idUsuario": user_id, "libro_id": libro_id
        })
        if existente.total > 0:
            raise ValueError("Este libro ya fue guardado por el usuario actual")
        guardado = GuardadoModel(fk_idUser=user_id, fk_idLibro=libro_id)
        return GuardadoRepository.save(guardado)

    @staticmethod
    def delete(id):
        guardado = GuardadoRepository.get_by_id(id)
        GuardadoRepository.delete(guardado)
