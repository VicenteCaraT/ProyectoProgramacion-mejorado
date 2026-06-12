from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from main.models.libro import Libro

class LibroSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Libro
        load_instance = True
        include_fk = True
