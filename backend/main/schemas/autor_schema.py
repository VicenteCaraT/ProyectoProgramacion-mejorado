from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from main.models.autor import Autor

class AutorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Autor
        load_instance = True
        include_fk = True
        