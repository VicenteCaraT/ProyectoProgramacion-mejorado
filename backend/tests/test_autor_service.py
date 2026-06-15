import pytest
from main.services import AutorService
from main.models import AutorModel

def test_create_autor_all_fields(app):
    with app.app_context():
        autor = AutorService.create({
            "nombre": "Gabriel",
            "apellido": "García Márquez",
            "apodo": "Gabo"
        })
        assert autor.idAutor is not None
        assert autor.nombre == "Gabriel"
        assert autor.apellido == "García Márquez"
        assert autor.apodo == "Gabo"

def test_get_autor(app):
    with app.app_context():
        autor = AutorService.create({
            "nombre": "Julio", "apellido": "Cortázar", "apodo": "Cronopio"
        })
        obtenido = AutorService.get_by_id(autor.idAutor)
        assert obtenido.nombre == "Julio"

def test_update_autor_nombre(app):
    with app.app_context():
        autor = AutorService.create({
            "nombre": "A", "apellido": "B", "apodo": "C"
        })
        actualizado = AutorService.update(autor.idAutor, {"nombre": "Nuevo"})
        assert actualizado.nombre == "Nuevo"
        assert actualizado.apellido == "B"

def test_update_autor_apellido(app):
    with app.app_context():
        autor = AutorService.create({
            "nombre": "A", "apellido": "B", "apodo": "C"
        })
        actualizado = AutorService.update(autor.idAutor, {"apellido": "Nuevo"})
        assert actualizado.apellido == "Nuevo"

def test_update_autor_apodo(app):
    with app.app_context():
        autor = AutorService.create({
            "nombre": "A", "apellido": "B", "apodo": "C"
        })
        actualizado = AutorService.update(autor.idAutor, {"apodo": "Nuevo"})
        assert actualizado.apodo == "Nuevo"

def test_delete_autor(app):
    with app.app_context():
        autor = AutorService.create({
            "nombre": "Julio", "apellido": "Cortázar", "apodo": "Cronopio"
        })
        autor_id = autor.idAutor
        AutorService.delete(autor_id)
        assert AutorService.get_by_id(autor_id) is None