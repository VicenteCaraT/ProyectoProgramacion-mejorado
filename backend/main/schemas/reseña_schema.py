from marshmallow import Schema, fields, validate


class ReseñaSchema(Schema):
    usuario = fields.Integer(required=True)
    libro = fields.Integer(required=True)
    fecha = fields.String(required=True)
    descripcion = fields.String(required=True, validate=validate.Length(min=1, max=255))
    valoracion = fields.String(required=True)
