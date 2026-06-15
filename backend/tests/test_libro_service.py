import pytest
from main.services import LibroService, AutorService

@pytest.fixture
def autor_data(app):
    with app.app_context():
        autor = AutorService.create({
            "nombre": "George", "apellido": "Orwell", "apodo": "Orwell"
        })
        return autor.idAutor

@pytest.fixture
def otro_autor(app):
    with app.app_context():
        autor = AutorService.create({
            "nombre": "Aldous", "apellido": "Huxley", "apodo": "Huxley"
        })
        return autor.idAutor

def test_create_libro_all_fields(app, autor_data):
    with app.app_context():
        libro = LibroService.create({
            "titulo": "1984", "cantidad": 5,
            "editorial": "Debolsillo", "genero": "Distopía",
            "sinopsis": "Una novela de vigilancia totalitaria",
            "img": "1984.jpg",
            "autor": [autor_data]
        })
        assert libro.idLibro is not None
        assert libro.titulo == "1984"
        assert libro.cantidad == 5
        assert libro.editorial == "Debolsillo"
        assert libro.genero == "Distopía"
        assert libro.sinopsis == "Una novela de vigilancia totalitaria"
        assert libro.book_img == "1984.jpg"

def test_get_libro(app, autor_data):
    with app.app_context():
        libro = LibroService.create({
            "titulo": "Rebelión", "cantidad": 3,
            "editorial": "SXXI", "genero": "Ficción",
            "sinopsis": "...", "img": "reb.jpg",
            "autor": [autor_data]
        })
        obtenido = LibroService.get_by_id(libro.idLibro)
        assert obtenido.titulo == "Rebelión"

def test_update_libro_titulo(app, autor_data):
    with app.app_context():
        libro = LibroService.create({
            "titulo": "Original", "cantidad": 1,
            "editorial": "Ed", "genero": "Gen",
            "sinopsis": "...", "img": "a.jpg",
            "autor": [autor_data]
        })
        actualizado = LibroService.update(libro.idLibro, {"titulo": "Nuevo"})
        assert actualizado.titulo == "Nuevo"
        assert actualizado.cantidad == 1

def test_update_libro_cantidad(app, autor_data):
    with app.app_context():
        libro = LibroService.create({
            "titulo": "T", "cantidad": 3,
            "editorial": "Ed", "genero": "Gen",
            "sinopsis": "...", "img": "a.jpg",
            "autor": [autor_data]
        })
        actualizado = LibroService.update(libro.idLibro, {"cantidad": 10})
        assert actualizado.cantidad == 10

def test_update_libro_editorial(app, autor_data):
    with app.app_context():
        libro = LibroService.create({
            "titulo": "T", "cantidad": 1,
            "editorial": "Original", "genero": "Gen",
            "sinopsis": "...", "img": "a.jpg",
            "autor": [autor_data]
        })
        actualizado = LibroService.update(libro.idLibro, {"editorial": "Nueva"})
        assert actualizado.editorial == "Nueva"

def test_update_libro_genero(app, autor_data):
    with app.app_context():
        libro = LibroService.create({
            "titulo": "T", "cantidad": 1,
            "editorial": "Ed", "genero": "Original",
            "sinopsis": "...", "img": "a.jpg",
            "autor": [autor_data]
        })
        actualizado = LibroService.update(libro.idLibro, {"genero": "Nuevo"})
        assert actualizado.genero == "Nuevo"

def test_update_libro_sinopsis(app, autor_data):
    with app.app_context():
        libro = LibroService.create({
            "titulo": "T", "cantidad": 1,
            "editorial": "Ed", "genero": "Gen",
            "sinopsis": "Original", "img": "a.jpg",
            "autor": [autor_data]
        })
        actualizado = LibroService.update(libro.idLibro, {"sinopsis": "Nueva"})
        assert actualizado.sinopsis == "Nueva"

def test_update_libro_img(app, autor_data):
    with app.app_context():
        libro = LibroService.create({
            "titulo": "T", "cantidad": 1,
            "editorial": "Ed", "genero": "Gen",
            "sinopsis": "...", "img": "old.jpg",
            "autor": [autor_data]
        })
        actualizado = LibroService.update(libro.idLibro, {"book_img": "new.jpg"})
        assert actualizado.book_img == "new.jpg"

def test_create_libro_autor_inexistente(app):
    with app.app_context():
        with pytest.raises(ValueError, match="no existe"):
            LibroService.create({
                "titulo": "Sin Autor", "cantidad": 1,
                "editorial": "Ed", "genero": "Test",
                "sinopsis": "...", "img": "x.jpg",
                "autor": [99999]
            })

def test_update_libro_autor_inexistente(app, autor_data):
    with app.app_context():
        libro = LibroService.create({
            "titulo": "T", "cantidad": 1,
            "editorial": "Ed", "genero": "Gen",
            "sinopsis": "...", "img": "a.jpg",
            "autor": [autor_data]
        })
        with pytest.raises(ValueError, match="no existe"):
            LibroService.update(libro.idLibro, {"autor": 99999})

def test_update_libro_autor(app, autor_data, otro_autor):
    with app.app_context():
        libro = LibroService.create({
            "titulo": "T", "cantidad": 1,
            "editorial": "Ed", "genero": "Gen",
            "sinopsis": "...", "img": "a.jpg",
            "autor": [autor_data]
        })
        actualizado = LibroService.update(libro.idLibro, {"autor": otro_autor})
        ids = [a.idAutor for a in actualizado.fk_idAutor]
        assert otro_autor in ids
        assert autor_data not in ids

def test_delete_libro(app, autor_data):
    with app.app_context():
        libro = LibroService.create({
            "titulo": "Temp", "cantidad": 1,
            "editorial": "Temp", "genero": "Test",
            "sinopsis": "...", "img": "t.jpg",
            "autor": [autor_data]
        })
        lid = libro.idLibro
        LibroService.delete(lid)
        assert LibroService.get_by_id(lid) is None

def test_get_all_pagination(app, autor_data):
    with app.app_context():
        for i in range(5):
            LibroService.create({
                "titulo": f"Libro {i}", "cantidad": i,
                "editorial": "Ed", "genero": "Test",
                "sinopsis": "...", "img": f"{i}.jpg",
                "autor": [autor_data]
            })
        result = LibroService.get_all({"page": 1, "per_page": 2})
        assert len(result.items) == 2
        assert result.total == 5
        assert result.pages == 3
