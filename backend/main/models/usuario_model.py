from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"
    idUser = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(60), nullable=False)
    contraseña = db.Column(db.String(60), nullable=False)
    nombre = db.Column(db.String(60), nullable=False)
    apellido = db.Column(db.String(60), nullable=False)
    dni = db.Column(db.Integer, nullable=False)
    telefono = db.Column(db.String(14), nullable=False)
    email = db.Column(db.String(60),  unique=True, index=True, nullable=False)
    rol = db.Column(db.String(30), nullable=False, server_default = "Pendiente")
    profile_img = db.Column(db.String(60))
    estado = db.Column(db.Boolean, nullable=False, default=False)
    notificaciones_user = db.relationship("Notificacion", back_populates="fk_user_notificacion", cascade="all, delete-orphan")
    prestamos_user = db.relationship("Prestamo", back_populates="fk_user_prestamo", cascade="all, delete-orphan")
    reseñas_user = db.relationship("Reseña", back_populates="fk_user_reseña", cascade="all, delete-orphan")
    guardados_user = db.relationship("Guardado", back_populates="fk_user_guardado", cascade="all, delete-orphan")
    
    @property
    def plain_password(self):
        raise AttributeError('Password cant be read')
    
    @plain_password.setter
    def plain_password(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)
    
    def validate_pass(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)
    
    @staticmethod
    def from_json(usuario_json):
        id = usuario_json.get("id")
        user = usuario_json.get("user")
        contraseña = usuario_json.get("contraseña")
        nombre = usuario_json.get("nombre")
        apellido = usuario_json.get("apellido")
        dni = usuario_json.get("dni")
        telefono = usuario_json.get("telefono")
        email = usuario_json.get("email")
        rol = usuario_json.get("rol")   
        img = usuario_json.get("img") #ver como manejar las imagenes
        estado = usuario_json.get("estado")    
        return Usuario(
            idUser=id,
            user=user,
            plain_password=contraseña,
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            telefono=telefono,
            email=email,
            rol=rol,
            profile_img=img,
            estado=estado
        )