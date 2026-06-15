from .. import db
from .libro_model import libros_autores

class Autor(db.Model):
    __tablename__ = "autores"
    idAutor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), nullable=False)
    apellido = db.Column(db.String(60), nullable=False)
    apodo = db.Column(db.String(60), nullable=False)

    @staticmethod
    def from_json(autor_json):
        id = autor_json.get("id")
        nombre = autor_json.get("nombre")
        apellido = autor_json.get("apellido")
        apodo = autor_json.get("apodo")
        return Autor(
            idAutor=id,
            nombre=nombre,
            apellido=apellido,
            apodo=apodo
        )