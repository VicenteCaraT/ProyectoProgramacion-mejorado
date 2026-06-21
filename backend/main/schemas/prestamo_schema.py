from marshmallow import Schema, fields, validate


class PrestamoSchema(Schema):
    usuario = fields.Integer(required=True)
    libro = fields.List(fields.Integer(), required=True)
    inicio_prestamo = fields.String(required=False)
    fin_prestamo = fields.String(required=False)
    estado = fields.String(required=False, validate=validate.OneOf(["Pendiente", "Activo", "Desactivado", "Terminado"]))
