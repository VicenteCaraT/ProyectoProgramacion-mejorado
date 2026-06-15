import pytest
from main.services import UsuarioService
from main.repositories import UsuarioRepository

def test_create_usuario_all_fields(app):
    with app.app_context():
        data = {
            "user": "jperez", "nombre": "Juan", "apellido": "Perez",
            "dni": 12345678, "telefono": "2611234567",
            "email": "juan@test.com", "rol": "Usuario", "estado": True,
            "contraseña": "pass123"
        }
        usuario = UsuarioService.create(data)
        assert usuario.idUser is not None
        assert usuario.user == "jperez"
        assert usuario.nombre == "Juan"
        assert usuario.apellido == "Perez"
        assert usuario.dni == 12345678
        assert usuario.telefono == "2611234567"
        assert usuario.email == "juan@test.com"
        assert usuario.rol == "Usuario"
        assert usuario.estado is True
        assert usuario.validate_pass("pass123") is True

def test_get_by_email(app):
    with app.app_context():
        UsuarioService.create({
            "user": "test", "nombre": "T", "apellido": "U",
            "dni": 11111111, "telefono": "2610000000",
            "email": "unique@test.com", "rol": "Admin",
            "contraseña": "pass123"
        })
        user = UsuarioRepository.get_by_email("unique@test.com")
        assert user is not None
        assert user.email == "unique@test.com"

        inexistente = UsuarioRepository.get_by_email("no@existe.com")
        assert inexistente is None

def _crear_usuario_base(app):
    return UsuarioService.create({
        "user": "original", "nombre": "Original", "apellido": "Uno",
        "dni": 22222222, "telefono": "2611111111",
        "email": "orig@test.com", "rol": "Usuario", "estado": True,
        "contraseña": "pass123"
    })

def test_update_usuario_user(app):
    u = _crear_usuario_base(app)
    actualizado = UsuarioService.update(u.idUser, {"user": "nuevouser"})
    assert actualizado.user == "nuevouser"

def test_update_usuario_nombre(app):
    u = _crear_usuario_base(app)
    actualizado = UsuarioService.update(u.idUser, {"nombre": "Modificado"})
    assert actualizado.nombre == "Modificado"

def test_update_usuario_apellido(app):
    u = _crear_usuario_base(app)
    actualizado = UsuarioService.update(u.idUser, {"apellido": "Nuevo"})
    assert actualizado.apellido == "Nuevo"

def test_update_usuario_dni(app):
    u = _crear_usuario_base(app)
    actualizado = UsuarioService.update(u.idUser, {"dni": 99999999})
    assert actualizado.dni == 99999999

def test_update_usuario_telefono(app):
    u = _crear_usuario_base(app)
    actualizado = UsuarioService.update(u.idUser, {"telefono": "2610000000"})
    assert actualizado.telefono == "2610000000"

def test_update_usuario_email(app):
    u = _crear_usuario_base(app)
    actualizado = UsuarioService.update(u.idUser, {"email": "nuevo@test.com"})
    assert actualizado.email == "nuevo@test.com"

def test_update_usuario_rol(app):
    u = _crear_usuario_base(app)
    actualizado = UsuarioService.update(u.idUser, {"rol": "Admin"})
    assert actualizado.rol == "Admin"

def test_update_usuario_estado(app):
    u = _crear_usuario_base(app)
    actualizado = UsuarioService.update(u.idUser, {"estado": False})
    assert actualizado.estado is False

def test_delete_usuario(app):
    with app.app_context():
        usuario = UsuarioService.create({
            "user": "delete", "nombre": "Del", "apellido": "Ete",
            "dni": 33333333, "telefono": "2612222222",
            "email": "delete@test.com", "contraseña": "pass123"
        })
        uid = usuario.idUser
        UsuarioService.delete(uid)
        assert UsuarioService.get_by_id(uid) is None

def test_password_hashing(app):
    with app.app_context():
        usuario = UsuarioService.create({
            "user": "pass", "nombre": "Pass", "apellido": "Word",
            "dni": 44444444, "telefono": "2613333333",
            "email": "pass@test.com", "contraseña": "secreta123"
        })
        assert usuario.validate_pass("secreta123") is True
        assert usuario.validate_pass("wrong") is False
