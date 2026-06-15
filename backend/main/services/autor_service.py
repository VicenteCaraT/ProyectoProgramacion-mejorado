from main.repositories import AutorRepository
from main.models import AutorModel

class AutorService:
    @staticmethod
    def get_by_id(id):
        return AutorRepository.get_by_id(id)

    @staticmethod
    def get_all(filters):
        return AutorRepository.get_all(
            page=filters.pop("page", 1),
            per_page=filters.pop("per_page", 10),
            filters=filters
        )

    @staticmethod
    def create(data):
        autor = AutorModel.from_json(data)
        return AutorRepository.save(autor)

    @staticmethod
    def update(id, data):
        autor = AutorRepository.get_by_id(id)
        for key, value in data.items():
            setattr(autor, key, value)
        return AutorRepository.save(autor)

    @staticmethod
    def delete(id):
        autor = AutorRepository.get_by_id(id)
        AutorRepository.delete(autor)
