from marshmallow import Schema, fields, validate


class AutorSchema(Schema):
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=60))
    apellido = fields.String(required=True, validate=validate.Length(min=1, max=60))
    apodo = fields.String(required=True, validate=validate.Length(min=1, max=60))
