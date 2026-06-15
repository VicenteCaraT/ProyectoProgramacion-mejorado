import pytest
from main.services import ReseñaService, LibroService, AutorService, UsuarioService

@pytest.fixture
def base_data(app):
    with app.app_context():
        autor = AutorService.create({
            "nombre": "Autor", "apellido": "Reseña", "apodo": "AR"
        })
        libro = LibroService.create({
            "titulo": "Libro Reseñable", "cantidad": 3,
            "editorial": "Ed", "genero": "Test",
            "sinopsis": "...", "img": "r.jpg",
            "autor": [autor.idAutor]
        })
        user = UsuarioService.create({
            "user": "reseña_user", "nombre": "R", "apellido": "User",
            "dni": 88888888, "telefono": "2617777777",
            "email": "reseña@test.com", "contraseña": "pass123"
        })
        return {"user_id": user.idUser, "libro_id": libro.idLibro}

from datetime import datetime

def test_create_reseña_usuario_inexistente(app, base_data):
    with app.app_context():
        with pytest.raises(ValueError, match="no existe"):
            ReseñaService.create({
                "usuario": 99999,
                "libro": base_data["libro_id"],
                "fecha": "15-06-2026",
                "descripcion": "Test",
                "valoracion": "3"
            })

def test_create_reseña_libro_inexistente(app, base_data):
    with app.app_context():
        with pytest.raises(ValueError, match="no existe"):
            ReseñaService.create({
                "usuario": base_data["user_id"],
                "libro": 99999,
                "fecha": "15-06-2026",
                "descripcion": "Test",
                "valoracion": "3"
            })

def test_create_reseña_all_fields(app, base_data):
    with app.app_context():
        data = {
            "usuario": base_data["user_id"],
            "libro": base_data["libro_id"],
            "fecha": "15-06-2026",
            "descripcion": "Muy buen libro",
            "valoracion": "5"
        }
        reseña = ReseñaService.create(data)
        assert reseña.idReseña is not None
        assert reseña.fk_idUser == base_data["user_id"]
        assert reseña.fk_idLibro == base_data["libro_id"]
        assert reseña.fecha == datetime(2026, 6, 15)
        assert reseña.descripcion == "Muy buen libro"
        assert reseña.valoracion == "5"

def test_get_reseña(app, base_data):
    with app.app_context():
        reseña = ReseñaService.create({
            "usuario": base_data["user_id"],
            "libro": base_data["libro_id"],
            "fecha": "15-06-2026",
            "descripcion": "Test", "valoracion": "4"
        })
        obtenido = ReseñaService.get_by_id(reseña.idReseña)
        assert obtenido.descripcion == "Test"

def test_update_reseña_descripcion(app, base_data):
    with app.app_context():
        reseña = ReseñaService.create({
            "usuario": base_data["user_id"],
            "libro": base_data["libro_id"],
            "fecha": "15-06-2026",
            "descripcion": "Original", "valoracion": "3"
        })
        actualizado = ReseñaService.update(reseña.idReseña, {"descripcion": "Actualizada"})
        assert actualizado.descripcion == "Actualizada"
        assert actualizado.valoracion == "3"

def test_update_reseña_valoracion(app, base_data):
    with app.app_context():
        reseña = ReseñaService.create({
            "usuario": base_data["user_id"],
            "libro": base_data["libro_id"],
            "fecha": "15-06-2026",
            "descripcion": "Test", "valoracion": "3"
        })
        actualizado = ReseñaService.update(reseña.idReseña, {"valoracion": "5"})
        assert actualizado.valoracion == "5"
        assert actualizado.descripcion == "Test"

def test_delete_reseña(app, base_data):
    with app.app_context():
        reseña = ReseñaService.create({
            "usuario": base_data["user_id"],
            "libro": base_data["libro_id"],
            "fecha": "15-06-2026",
            "descripcion": "Eliminar",
            "valoracion": "2"
        })
        rid = reseña.idReseña
        ReseñaService.delete(rid)
        assert ReseñaService.get_by_id(rid) is None

def test_get_all_reseñas(app, base_data):
    with app.app_context():
        ReseñaService.create({
            "usuario": base_data["user_id"], "libro": base_data["libro_id"],
            "fecha": "01-01-2026", "descripcion": "A", "valoracion": "4"
        })
        ReseñaService.create({
            "usuario": base_data["user_id"], "libro": base_data["libro_id"],
            "fecha": "02-01-2026", "descripcion": "B", "valoracion": "5"
        })
        result = ReseñaService.get_all({"page": 1, "per_page": 10})
        assert result.total >= 2
