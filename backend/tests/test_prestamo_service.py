import pytest
from main.services import PrestamoService, LibroService, AutorService
from datetime import datetime, timedelta

@pytest.fixture
def libro_data(app):
    with app.app_context():
        autor = AutorService.create({
            "nombre": "Autor", "apellido": "Test", "apodo": "AT"
        })
        libro = LibroService.create({
            "titulo": "Libro Test", "cantidad": 5,
            "editorial": "Ed", "genero": "Test",
            "sinopsis": "...", "img": "test.jpg",
            "autor": [autor.idAutor]
        })
        return {"libro_id": libro.idLibro, "stock_inicial": libro.cantidad}

@pytest.fixture
def usuario_data(app):
    from main.services import UsuarioService
    with app.app_context():
        user = UsuarioService.create({
            "user": "lector", "nombre": "Lector", "apellido": "Uno",
            "dni": 55555555, "telefono": "2614444444",
            "email": "lector@test.com", "contraseña": "pass123"
        })
        return user.idUser

def test_create_prestamo_libro_inexistente(app, usuario_data):
    with app.app_context():
        with pytest.raises(ValueError, match="no existe"):
            PrestamoService.create({
                "usuario": usuario_data,
                "libro": 99999
            })

def test_create_prestamo_usuario_inexistente(app, libro_data):
    with app.app_context():
        with pytest.raises(ValueError, match="no existe"):
            PrestamoService.create({
                "usuario": 99999,
                "libro": libro_data["libro_id"]
            })

def test_update_prestamo_libro_inexistente(app, libro_data, usuario_data):
    with app.app_context():
        prestamo = PrestamoService.create({
            "usuario": usuario_data,
            "libro": libro_data["libro_id"]
        })
        with pytest.raises(ValueError, match="no existe"):
            PrestamoService.update(prestamo.idPrestamo, {"libro": 99999})

def test_create_prestamo(app, libro_data, usuario_data):
    with app.app_context():
        prestamo = PrestamoService.create({
            "usuario": usuario_data,
            "libro": libro_data["libro_id"]
        })
        assert prestamo.idPrestamo is not None
        assert prestamo.estado == "Pendiente"

def test_create_reduces_stock_when_activated(app, libro_data, usuario_data):
    with app.app_context():
        prestamo = PrestamoService.create({
            "usuario": usuario_data,
            "libro": libro_data["libro_id"]
        })
        # Activar préstamo
        prestamo = PrestamoService.update(prestamo.idPrestamo, {"estado": "Activo"})
        libro = LibroService.get_by_id(libro_data["libro_id"])
        assert libro.cantidad == libro_data["stock_inicial"] - 1

def test_deactivate_returns_stock(app, libro_data, usuario_data):
    with app.app_context():
        prestamo = PrestamoService.create({
            "usuario": usuario_data,
            "libro": libro_data["libro_id"]
        })
        prestamo = PrestamoService.update(prestamo.idPrestamo, {"estado": "Activo"})
        prestamo = PrestamoService.update(prestamo.idPrestamo, {"estado": "Desactivado"})
        libro = LibroService.get_by_id(libro_data["libro_id"])
        assert libro.cantidad == libro_data["stock_inicial"]

def test_delete_returns_stock(app, libro_data, usuario_data):
    with app.app_context():
        prestamo = PrestamoService.create({
            "usuario": usuario_data,
            "libro": libro_data["libro_id"]
        })
        prestamo = PrestamoService.update(prestamo.idPrestamo, {"estado": "Activo"})
        PrestamoService.delete(prestamo.idPrestamo)
        libro = LibroService.get_by_id(libro_data["libro_id"])
        assert libro.cantidad == libro_data["stock_inicial"]

def test_default_dates(app, libro_data, usuario_data):
    with app.app_context():
        prestamo = PrestamoService.create({
            "usuario": usuario_data,
            "libro": libro_data["libro_id"]
        })
        hoy = datetime.today()
        assert prestamo.inicio_prestamo.day == hoy.day
        assert (prestamo.fin_prestamo - prestamo.inicio_prestamo).days == 30

def _crear_prestamo(app, libro_data, usuario_data):
    return PrestamoService.create({
        "usuario": usuario_data,
        "libro": libro_data["libro_id"]
    })

def test_update_prestamo_inicio_prestamo(app, libro_data, usuario_data):
    with app.app_context():
        prestamo = _crear_prestamo(app, libro_data, usuario_data)
        nueva_fecha = "01-01-2026"
        actualizado = PrestamoService.update(prestamo.idPrestamo, {"inicio_prestamo": nueva_fecha})
        assert actualizado.inicio_prestamo == datetime(2026, 1, 1)

def test_update_prestamo_fin_prestamo(app, libro_data, usuario_data):
    with app.app_context():
        prestamo = _crear_prestamo(app, libro_data, usuario_data)
        nueva_fecha = "01-06-2026"
        actualizado = PrestamoService.update(prestamo.idPrestamo, {"fin_prestamo": nueva_fecha})
        assert actualizado.fin_prestamo == datetime(2026, 6, 1)

def test_update_prestamo_libro(app, libro_data, usuario_data):
    with app.app_context():
        autor2 = AutorService.create({
            "nombre": "Otro", "apellido": "Autor", "apodo": "OA"
        })
        libro2 = LibroService.create({
            "titulo": "Otro Libro", "cantidad": 2,
            "editorial": "Ed", "genero": "Test",
            "sinopsis": "...", "img": "o.jpg",
            "autor": [autor2.idAutor]
        })
        prestamo = _crear_prestamo(app, libro_data, usuario_data)
        actualizado = PrestamoService.update(prestamo.idPrestamo, {"libro": [libro2.idLibro]})
        ids = [l.idLibro for l in actualizado.fk_idLibro]
        assert libro2.idLibro in ids
        assert len(actualizado.fk_idLibro) == 1

def test_expire_overdue(app, libro_data, usuario_data):
    with app.app_context():
        prestamo = PrestamoService.create({
            "usuario": usuario_data,
            "libro": libro_data["libro_id"]
        })
        prestamo = PrestamoService.update(prestamo.idPrestamo, {"estado": "Activo"})
        # Forzar fecha de fin al pasado
        from main.repositories import PrestamoRepository
        from main.models import PrestamoModel
        prestamo.fin_prestamo = datetime.today() - timedelta(days=1)
        PrestamoRepository.save(prestamo)

        cambios = PrestamoService.expire_overdue()
        assert cambios >= 1

        prestamo = PrestamoService.get_by_id(prestamo.idPrestamo)
        assert prestamo.estado == "Terminado"
