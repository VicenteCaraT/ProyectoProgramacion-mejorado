from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from main.models.guardado import Guardado

class GuardadoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Guardado
        load_instance = True
        include_fk = True