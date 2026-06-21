from marshmallow import Schema, fields, validate


class LibroSchema(Schema):
    titulo = fields.String(required=True, validate=validate.Length(min=1))
    cantidad = fields.Integer(required=True, validate=validate.Range(min=0))
    editorial = fields.String(required=True, validate=validate.Length(min=1, max=60))
    genero = fields.String(required=True, validate=validate.Length(min=1, max=60))
    sinopsis = fields.String(required=True, validate=validate.Length(min=1, max=300))
    img = fields.String(required=True)
    autor = fields.List(fields.Integer(), required=True)
