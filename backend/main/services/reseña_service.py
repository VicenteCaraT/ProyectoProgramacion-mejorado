from main.repositories import ReseñaRepository, UsuarioRepository, LibroRepository
from main.models import ReseñaModel

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
        user_id = data.get("usuario")
        libro_id = data.get("libro")
        if UsuarioRepository.get_by_id(user_id) is None:
            raise ValueError(f"El usuario ID {user_id} no existe")
        if LibroRepository.get_by_id(libro_id) is None:
            raise ValueError(f"El libro ID {libro_id} no existe")
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
