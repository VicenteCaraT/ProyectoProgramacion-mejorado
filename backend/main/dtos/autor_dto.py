class AutorDTO:
    @staticmethod
    def full(autor):
        return {
            "id": autor.idAutor,
            "nombre": autor.nombre,
            "apellido": autor.apellido,
            "apodo": autor.apodo
        }

    @staticmethod
    def short(autor):
        return {"apodo": autor.apodo}
