from .. import db
from datetime import datetime

class Reseña(db.Model):
    __tablename__ = "reseñas"
    idReseña = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fk_idUser = db.Column(db.Integer, db.ForeignKey("usuarios.idUser"), nullable=False)
    fk_user_reseña = db.relationship("Usuario", back_populates="reseñas_user", uselist=False, single_parent=True)
    fk_idLibro = db.Column(db.Integer, db.ForeignKey("libros.idLibro"), nullable=False)
    fk_libro_reseña = db.relationship("Libro", back_populates="reseñas_libro", uselist=False, single_parent=True)
    fecha = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    valoracion = db.Column(db.String, nullable=False)
    

    def __repr__(self):
        return f"<id: {self.idReseña}, Usuario: {self.fk_idUser}, Libro: {self.fk_idLibro}, Fecha: {self.fecha}, Descripcion: {self.descripcion}, Valoracion: {self.valoracion}"
    
    @staticmethod
    def from_json(reseña_json):
        id = reseña_json.get("id")
        usuario = reseña_json.get("usuario")
        libro = reseña_json.get("libro")
        fecha = datetime.strptime(reseña_json.get("fecha"), "%d-%m-%Y")
        descripcion = reseña_json.get("descripcion")
        valoracion = reseña_json.get("valoracion")
        return Reseña(
            idReseña=id,
            fk_idUser=usuario,
            fk_idLibro=libro,
            fecha=fecha,
            descripcion=descripcion,
            valoracion=valoracion
        )