from .. import db

libros_autores = db.Table("libros_autores",
    db.Column("id_autor",db.Integer,db.ForeignKey("autores.idAutor"), primary_key=True),
    db.Column("id_libro", db.Integer, db.ForeignKey("libros.idLibro"), primary_key=True)
)

class Libro(db.Model):
    __tablename__ = "libros"
    idLibro = db.Column(db.Integer, primary_key=True)
    book_img = db.Column(db.String, nullable=False)
    titulo = db.Column(db.String, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fk_idAutor = db.relationship("Autor", secondary=libros_autores, backref=db.backref('autores', lazy="dynamic"))
    editorial = db.Column(db.String(60), nullable=False)
    genero = db.Column(db.String(60), nullable=False)
    sinopsis = db.Column(db.String(300), nullable=False)
    reseñas_libro = db.relationship("Reseña", back_populates="fk_libro_reseña", cascade="all, delete-orphan")
    guardados_libro = db.relationship("Guardado", back_populates="fk_libro_guardado", cascade="all, delete-orphan")

    @staticmethod
    def from_json(libro_json):
        id = libro_json.get("id")
        img = libro_json.get("img")
        titulo = libro_json.get("titulo")
        cantidad = libro_json.get("cantidad")
        editorial = libro_json.get("editorial")
        genero = libro_json.get("genero")
        sinopsis = libro_json.get("sinopsis")
        return Libro(
            idLibro=id,
            book_img=img,
            titulo=titulo,
            cantidad=cantidad,
            editorial=editorial,
            genero=genero,
            sinopsis=sinopsis
        )