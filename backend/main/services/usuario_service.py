from main.repositories import UsuarioRepository
from main.models import UsuarioModel
from .base_service import BaseService

class UsuarioService(BaseService):
    repository = UsuarioRepository
    model = UsuarioModel