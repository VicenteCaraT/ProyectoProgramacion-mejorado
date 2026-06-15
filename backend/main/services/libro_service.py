from main.repositories import LibroRepository, AutorRepository
from main.models import LibroModel

class LibroService:
    @staticmethod
    def get_by_id(id):
        return LibroRepository.get_by_id(id)

    @staticmethod
    def get_all(filters):
        return LibroRepository.get_all(
            page=filters.pop("page", 1),
            per_page=filters.pop("per_page", 10),
            filters=filters
        )

    @staticmethod
    def create(data):
        autor_ids = data.pop("autor", None)
        libro = LibroModel.from_json(data)
        if autor_ids:
            if not isinstance(autor_ids, list):
                autor_ids = [autor_ids]
            autores = []
            for aid in autor_ids:
                autor = AutorRepository.get_by_id(aid)
                if autor is None:
                    raise ValueError(f"El autor ID {aid} no existe")
                autores.append(autor)
            libro.fk_idAutor.extend(autores)
        return LibroRepository.save(libro)

    @staticmethod
    def update(id, data):
        libro = LibroRepository.get_by_id(id)
        autor_ids = data.pop("autor", None)
        for key, value in data.items():
            if key != "autor":
                setattr(libro, key, value)
        if autor_ids:
            if not isinstance(autor_ids, list):
                autor_ids = [autor_ids]
            autores = []
            for aid in autor_ids:
                autor = AutorRepository.get_by_id(aid)
                if autor is None:
                    raise ValueError(f"El autor ID {aid} no existe")
                autores.append(autor)
            libro.fk_idAutor = autores
        return LibroRepository.save(libro)

    @staticmethod
    def delete(id):
        libro = LibroRepository.get_by_id(id)
        LibroRepository.delete(libro)
