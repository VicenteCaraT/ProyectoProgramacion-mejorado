from marshmallow import Schema, fields


class GuardadoSchema(Schema):
    libro = fields.Integer(required=True)
