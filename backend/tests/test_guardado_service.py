import pytest
from main.services import GuardadoService, LibroService, AutorService, UsuarioService

@pytest.fixture
def base_data(app):
    with app.app_context():
        autor = AutorService.create({
            "nombre": "A", "apellido": "B", "apodo": "C"
        })
        libro = LibroService.create({
            "titulo": "Guardable", "cantidad": 1,
            "editorial": "Ed", "genero": "Test",
            "sinopsis": "...",             "img": "g.jpg",
            "autor": [autor.idAutor]
        })
        user = UsuarioService.create({
            "user": "save_user", "nombre": "S", "apellido": "U",
            "dni": 66666666, "telefono": "2615555555",
            "email": "save@test.com", "contraseña": "pass123"
        })
        return {"user_id": user.idUser, "libro_id": libro.idLibro}

def test_create_guardado_usuario_inexistente(app, base_data):
    with app.app_context():
        with pytest.raises(ValueError, match="no existe"):
            GuardadoService.create(99999, base_data["libro_id"])

def test_create_guardado_libro_inexistente(app, base_data):
    with app.app_context():
        with pytest.raises(ValueError, match="no existe"):
            GuardadoService.create(base_data["user_id"], 99999)

def test_create_guardado(app, base_data):
    with app.app_context():
        guardado = GuardadoService.create(
            base_data["user_id"], base_data["libro_id"]
        )
        assert guardado.idGuardado is not None
        assert guardado.fk_idUser == base_data["user_id"]
        assert guardado.fk_idLibro == base_data["libro_id"]

def test_duplicate_guardado(app, base_data):
    with app.app_context():
        GuardadoService.create(base_data["user_id"], base_data["libro_id"])
        with pytest.raises(ValueError, match="ya fue guardado"):
            GuardadoService.create(base_data["user_id"], base_data["libro_id"])

def test_delete_guardado(app, base_data):
    with app.app_context():
        guardado = GuardadoService.create(
            base_data["user_id"], base_data["libro_id"]
        )
        gid = guardado.idGuardado
        GuardadoService.delete(gid)
        assert GuardadoService.get_by_id(gid) is None
