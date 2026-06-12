from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from main.models.notificacion import Notificacion

class NotificacionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Notificacion
        load_instance = True
        include_fk = True