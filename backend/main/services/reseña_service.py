from main.repositories import ReseñaRepository
from main.models import ReseñaModel, UsuarioModel, LibroModel

class ReseñaService:
    @staticmethod
    def get_by_id(id):
        return ReseñaRepository.get_by_id(id)

    @staticmethod
    def get_all(filters):
        return ReseñaRepository.get_all(
            page=filters.pop("page", 1),
            per_page=filters.pop("per_page", 10),
            filters=filters
        )

    @staticmethod
    def create(data):
        reseña = ReseñaModel.from_json(data)
        return ReseñaRepository.save(reseña)

    @staticmethod
    def update(id, data):
        reseña = ReseñaRepository.get_by_id(id)
        for key, value in data.items():
            setattr(reseña, key, value)
        return ReseñaRepository.save(reseña)

    @staticmethod
    def delete(id):
        reseña = ReseñaRepository.get_by_id(id)
        ReseñaRepository.delete(reseña)
