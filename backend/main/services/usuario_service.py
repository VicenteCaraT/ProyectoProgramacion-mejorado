from main.repositories import UsuarioRepository
from main.models import UsuarioModel

class UsuarioService:
    @staticmethod
    def get_by_id(id):
        return UsuarioRepository.get_by_id(id)

    @staticmethod
    def get_all(filters):
        return UsuarioRepository.get_all(
            page=filters.pop("page", 1),
            per_page=filters.pop("per_page", 10),
            filters=filters
        )

    @staticmethod
    def create(data):
        usuario = UsuarioModel.from_json(data)
        return UsuarioRepository.save(usuario)

    @staticmethod
    def update(id, data):
        usuario = UsuarioRepository.get_by_id(id)
        for key, value in data.items():
            setattr(usuario, key, value)
        return UsuarioRepository.save(usuario)

    @staticmethod
    def delete(id):
        usuario = UsuarioRepository.get_by_id(id)
        UsuarioRepository.delete(usuario)
