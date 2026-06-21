from marshmallow import Schema, fields, validate, validates, ValidationError
import re


class UsuarioSchema(Schema):
    user = fields.String(required=True, validate=validate.Length(min=3, max=60))
    contraseña = fields.String(required=True, validate=validate.Length(min=6, max=128))
    nombre = fields.String(required=True, validate=validate.Length(min=1, max=60))
    apellido = fields.String(required=True, validate=validate.Length(min=1, max=60))
    dni = fields.Integer(required=True)
    telefono = fields.String(required=True, validate=validate.Length(min=7, max=14))
    email = fields.Email(required=True)
    rol = fields.String(required=True, validate=validate.OneOf(["Admin", "Usuario", "Pendiente"]))
    img = fields.String(required=False)
    estado = fields.Boolean(required=False)
