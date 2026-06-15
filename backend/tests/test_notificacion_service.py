import pytest
from main.services import NotificacionService, UsuarioService

@pytest.fixture
def usuario_data(app):
    with app.app_context():
        user = UsuarioService.create({
            "user": "notif_user", "nombre": "N", "apellido": "User",
            "dni": 77777777, "telefono": "2616666666",
            "email": "notif@test.com", "contraseña": "pass123"
        })
        return user.idUser

def test_create_notificacion_usuario_inexistente(app):
    with app.app_context():
        with pytest.raises(ValueError, match="no existe"):
            NotificacionService.create({
                "usuario": 99999,
                "descripcion": "Test"
            })

def test_create_and_get_notificacion(app, usuario_data):
    with app.app_context():
        data = {
            "usuario": usuario_data,
            "descripcion": "Libro devuelto con exito"
        }
        notif = NotificacionService.create(data)
        assert notif.idNotificacion is not None
        assert notif.fk_idUser == usuario_data
        assert notif.descripcion == "Libro devuelto con exito"

        obtenido = NotificacionService.get_by_id(notif.idNotificacion)
        assert obtenido.descripcion == "Libro devuelto con exito"

def test_get_all_notificaciones(app, usuario_data):
    with app.app_context():
        NotificacionService.create({"usuario": usuario_data, "descripcion": "A"})
        NotificacionService.create({"usuario": usuario_data, "descripcion": "B"})
        result = NotificacionService.get_all({"page": 1, "per_page": 10})
        assert result.total >= 2

def test_delete_notificacion(app, usuario_data):
    with app.app_context():
        notif = NotificacionService.create({
            "usuario": usuario_data,
            "descripcion": "Temp"
        })
        nid = notif.idNotificacion
        NotificacionService.delete(nid)
        assert NotificacionService.get_by_id(nid) is None
