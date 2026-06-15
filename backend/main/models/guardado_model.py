from .. import db
from . import UsuarioModel
from . import LibroModel

class Guardado(db.Model):
    __tablename__= "guardados"
    
    idGuardado = db.Column(db.Integer, primary_key=True)
    fk_idUser = db.Column(db.Integer, db.ForeignKey("usuarios.idUser"), nullable=False)
    fk_user_guardado = db.relationship("Usuario", back_populates="guardados_user", uselist=False, single_parent=True)
    fk_idLibro = db.Column(db.Integer, db.ForeignKey("libros.idLibro"), nullable=False)
    fk_libro_guardado = db.relationship("Libro", back_populates="guardados_libro", uselist=False, single_parent=True)
    
    def __repr__(self):
        return f"<id: {self.idGuardado}, Usuario: {self.fk_idUser}, Libro: {self.fk_idLibro}"
    
    def to_json(self):
        guardado_json = {
            "id" : int(self.idGuardado),
            "usuario": self.fk_user_guardado.to_json(),
            "libro": self.fk_libro_guardado.to_json()
        }
        return guardado_json
    
    @staticmethod
    def from_json(guardado_json):
        id = guardado_json.get("id")
        usuario = guardado_json.get("usuario")
        libro = guardado_json.get("libro")
        return Guardado(
            idGuardado=id,
            fk_idUser=usuario,
            fk_idLibro=libro
        )