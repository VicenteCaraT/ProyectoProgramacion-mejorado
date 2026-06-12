from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from main.models.prestamo import Prestamo

class PrestamoSchema(SQLAlchemyAutoSchema):
    class Meta: 
        model = Prestamo
        load_instance = True
        include_fk = True
        
        