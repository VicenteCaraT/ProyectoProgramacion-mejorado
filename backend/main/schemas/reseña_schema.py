from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from main.models.reseña import Reseña

class ReseñaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Reseña
        load_instance = True
        include_fk = True