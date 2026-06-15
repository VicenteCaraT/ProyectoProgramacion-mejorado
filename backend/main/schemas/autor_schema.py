from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from main.models.autor_model import Autor

class AutorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Autor
        load_instance = True
        include_fk = True
        