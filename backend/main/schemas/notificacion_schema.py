from marshmallow import Schema, fields, validate


class NotificacionSchema(Schema):
    usuario = fields.Integer(required=True)
    descripcion = fields.String(required=True, validate=validate.Length(min=1, max=255))
