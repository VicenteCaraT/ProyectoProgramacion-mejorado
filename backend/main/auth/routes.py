from flask import request, jsonify, Blueprint
from main.models import UsuarioModel
from main.repositories import UsuarioRepository
from main.dtos import UsuarioDTO
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from main.mail.functions import sendMail
from marshmallow import ValidationError
from main.schemas import UsuarioSchema

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    user = UsuarioRepository.get_by_email(request.get_json().get("email"))
    if not user or not user.validate_pass(request.get_json().get("contraseña")):
        return {"message": "Incorrect password"}, 401
    access_token = create_access_token(identity=user)
    return {
        'id': str(user.idUser),
        'email': user.email,
        'access_token': access_token
    }, 200

@auth.route('/register', methods=['POST'])
def register():
    schema = UsuarioSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as e:
        return {"message": "Datos inválidos", "errors": e.messages}, 422
    user = UsuarioModel.from_json(data)
    if UsuarioRepository.exists_by_email(user.email):
        return {"message": "Duplicated mail"}, 409
    try:
        UsuarioRepository.save(user)
        sendMail([user.email], "Wellcome!", "register", user=user)
    except Exception as error:
        return {"message": str(error)}, 409
    return UsuarioDTO.full(user), 201