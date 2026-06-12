from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from main.models.usuario import Usuario

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_fk = True
        exclude = ['contraseña']
