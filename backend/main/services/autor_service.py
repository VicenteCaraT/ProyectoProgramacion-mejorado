from main.repositories import AutorRepository
from main.models import AutorModel
from .base_service import BaseService


class AutorService(BaseService):
    repository = AutorRepository
    model = AutorModel
