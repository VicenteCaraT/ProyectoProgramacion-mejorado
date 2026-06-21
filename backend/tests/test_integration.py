### TEST LOGIN ###
def test_login(client, app):
    with app.app_context():
        from main.models import UsuarioModel
        from main.repositories import UsuarioRepository
        user = UsuarioModel(
            user="test", nombre="Test", apellido="User",
            dni=12345678, telefono="123456789", email="login@test.com",
            rol="Admin", estado=True
        )
        user.plain_password = "test123"
        UsuarioRepository.save(user)

    resp = client.post("/auth/login", json={
        "email": "login@test.com", "contraseña": "test123"
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data
    assert data["email"] == "login@test.com"

def test_login_wrong_password(client, app):
    with app.app_context():
        from main.models import UsuarioModel
        from main.repositories import UsuarioRepository
        user = UsuarioModel(
            user="test", nombre="Test", apellido="User",
            dni=12345678, telefono="123456789", email="login2@test.com",
            rol="Admin", estado=True
        )
        user.plain_password = "test123"
        UsuarioRepository.save(user)

    resp = client.post("/auth/login", json={
        "email": "login2@test.com", "contraseña": "wrong"
    })
    assert resp.status_code == 401

### TEST REGISTER ###
def test_register(client):
    resp = client.post("/auth/register", json={
        "user": "newuser", "nombre": "Nuevo", "apellido": "User",
        "dni": 99999999, "telefono": "2619999999",
        "email": "newuser@test.com", "contraseña": "pass123",
        "rol": "Usuario", "estado": True
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["email"] == "newuser@test.com"
    assert data["user"] == "newuser"

def test_register_duplicate_email(client, app):
    with app.app_context():
        from main.models import UsuarioModel
        from main.repositories import UsuarioRepository
        user = UsuarioModel(
            user="existing", nombre="Exist", apellido="User",
            dni=11111111, telefono="2611111111",
            email="dup@test.com", rol="Usuario", estado=True
        )
        user.plain_password = "pass123"
        UsuarioRepository.save(user)

    resp = client.post("/auth/register", json={
        "user": "other", "nombre": "Otro", "apellido": "User",
        "dni": 22222222, "telefono": "2612222222",
        "email": "dup@test.com", "contraseña": "pass456",
        "rol": "Usuario", "estado": True
    })
    assert resp.status_code == 409

### TEST AUTOR ###
def test_autor_create_and_get(client, auth_headers):
    resp = client.post("/autores", json={
        "nombre": "Carl Gustav", "apellido": "Jung", "apodo": "Jung"
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.get_json()
    autor_id = data["autor"]["id"]

    resp = client.get(f"/autor/{autor_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["autor"]["nombre"] == "Carl Gustav"

def test_autor_list(client, auth_headers):
    client.post("/autores", json={
        "nombre": "A", "apellido": "B", "apodo": "C"
    }, headers=auth_headers)
    client.post("/autores", json={
        "nombre": "D", "apellido": "E", "apodo": "F"
    }, headers=auth_headers)

    resp = client.get("/autores", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["total"] == 2

def test_autor_update(client, auth_headers):
    resp = client.post("/autores", json={
        "nombre": "Original", "apellido": "A", "apodo": "O"
    }, headers=auth_headers)
    autor_id = resp.get_json()["autor"]["id"]

    resp = client.put(f"/autor/{autor_id}", json={
        "nombre": "Modificado"
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["autor"]["nombre"] == "Modificado"

def test_autor_delete(client, auth_headers):
    resp = client.post("/autores", json={
        "nombre": "Temp", "apellido": "T", "apodo": "T"
    }, headers=auth_headers)
    autor_id = resp.get_json()["autor"]["id"]

    resp = client.delete(f"/autor/{autor_id}", headers=auth_headers)
    assert resp.status_code == 204

def test_prestamo_create_and_get(client, auth_headers, app):
    with app.app_context():
        from main.services import UsuarioService, AutorService, LibroService
        usuario = UsuarioService.create({
            "user": "VicenCara", "contraseña": "admin123",
            "nombre": "Vicente", "apellido": "Cara",
            "dni": 123409123, "telefono": "2610000000",
            "email": "vicenprest@email.com",
            "rol": "Admin", "img": "img.png", "estado": True
        })
        autor = AutorService.create({"nombre": "A", "apellido": "B", "apodo": "C"})
        libro = LibroService.create({
            "titulo": "Mi Libro", "cantidad": 3,
            "editorial": "Ed", "genero": "Test",
            "sinopsis": "...", "img": "img.jpg",
            "autor": [autor.idAutor]
        })
        _user_id = usuario.idUser
        _libro_id = libro.idLibro

    resp = client.post("/prestamos", json={
        "usuario": _user_id,
        "libro": [_libro_id]
    }, headers=auth_headers)
    assert resp.status_code == 201
    prestamo_id = resp.get_json()["prestamo"]["id"]

    resp = client.get(f"/prestamo/{prestamo_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["estado"] == "Pendiente"

def test_autor_unauthorized(client):
    resp = client.post("/autores", json={
        "nombre": "X", "apellido": "Y", "apodo": "Z"
    })
    assert resp.status_code == 401


### TEST LIBROS ###
def test_libros_list(client, auth_headers):
    resp = client.get("/libros", headers=auth_headers)
    assert resp.status_code == 200

def test_libro_create_and_get(client, auth_headers, app):
    with app.app_context():
        from main.services import AutorService
        autor = AutorService.create({"nombre": "A", "apellido": "B", "apodo": "C"})
        autor_id = autor.idAutor
    resp = client.post("/libros", json={
        "titulo": "Mi Libro", "cantidad": 3,
        "editorial": "Ed", "genero": "Test",
        "sinopsis": "...", "img": "img.jpg",
        "autor": [autor_id]
    }, headers=auth_headers)
    assert resp.status_code == 201
    libro_id = resp.get_json()["libro"]["id"]
    resp = client.get(f"/libro/{libro_id}", headers=auth_headers)
    assert resp.get_json()["titulo"] == "Mi Libro"

def test_libro_update(client, auth_headers, app):
    with app.app_context():
        from main.services import AutorService
        autor = AutorService.create({"nombre": "A", "apellido": "B", "apodo": "C"})
        autor_id = autor.idAutor
    resp = client.post("/libros", json={
        "titulo": "Mi Libro", "cantidad": 3,
        "editorial": "Ed", "genero": "Test",
        "sinopsis": "...", "img": "img.jpg",
        "autor": [autor_id]
    }, headers=auth_headers)
    libro_id = resp.get_json()["libro"]["id"]
    resp = client.put(f"/libro/{libro_id}", json={"titulo": "Nuevo"},headers=auth_headers)
    assert resp.get_json()["libro"]["titulo"] == "Nuevo"

def test_libro_delete(client, auth_headers, app):
    with app.app_context():
        from main.services import AutorService
        autor = AutorService.create({"nombre": "A", "apellido": "B", "apodo": "C"})
        autor_id = autor.idAutor
    resp = client.post("/libros", json={
        "titulo": "Mi Libro", "cantidad": 3,
        "editorial": "Ed", "genero": "Test",
        "sinopsis": "...", "img": "img.jpg",
        "autor": [autor_id]
    }, headers=auth_headers)
    libro_id = resp.get_json()["libro"]["id"]
    resp = client.delete(f"/libro/{libro_id}", headers=auth_headers)
    assert resp.status_code == 204

def test_libro_unauthorized(client):
    resp = client.post("/libros", json={
        "titulo": "X", "cantidad": 1,
        "editorial": "E", "genero": "G",
        "sinopsis": "...", "img": "x.jpg", "autor": [999]
    })
    assert resp.status_code == 401

    resp = client.put("/libro/1", json={"titulo": "Nuevo"})
    assert resp.status_code == 401

    resp = client.delete("/libro/1")
    assert resp.status_code == 401

### TEST PRESTAMO ###
def test_prestamos_list(client, auth_headers):
    resp = client.get("/prestamos", headers=auth_headers)
    assert resp.status_code == 200

def test_prestamo_unauthorized(client):
    resp = client.post("/prestamos", json={
        "usuario": 1, "libro": [1]
    })
    assert resp.status_code == 401

    resp = client.put("/prestamo/1", json={"estado": "Activo"})
    assert resp.status_code == 401

    resp = client.delete("/prestamo/1")
    assert resp.status_code == 401

def test_prestamo_update(client, auth_headers, app):
    with app.app_context():
        from main.services import UsuarioService, AutorService, LibroService
        usuario = UsuarioService.create({
            "user": "VicenCara", "contraseña": "admin123",
            "nombre": "Vicente", "apellido": "Cara",
            "dni": 123409123, "telefono": "2610000000",
            "email": "vicenprest@email.com",
            "rol": "Admin", "img": "img.png", "estado": True
        })
        autor = AutorService.create({"nombre": "A", "apellido": "B", "apodo": "C"})
        libro = LibroService.create({
            "titulo": "Mi Libro", "cantidad": 3,
            "editorial": "Ed", "genero": "Test",
            "sinopsis": "...", "img": "img.jpg",
            "autor": [autor.idAutor]
        })
        _user_id = usuario.idUser
        _libro_id = libro.idLibro
    resp = client.post("/prestamos", json={
        "usuario": _user_id, "libro": [_libro_id]
    }, headers=auth_headers)
    assert resp.status_code == 201
    prestamo_id = resp.get_json()["prestamo"]["id"]

    resp = client.put(f"/prestamo/{prestamo_id}", json={
        "estado": "Activo"
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["prestamo"]["estado"] == "Activo"
    
def test_prestamo_delete(client, auth_headers, app):
    with app.app_context():
        from main.services import UsuarioService, AutorService, LibroService
        usuario = UsuarioService.create({
            "user": "VicenCara", "contraseña": "admin123",
            "nombre": "Vicente", "apellido": "Cara",
            "dni": 123409123, "telefono": "2610000000",
            "email": "vicenprest@email.com",
            "rol": "Admin", "img": "img.png", "estado": True
        })
        autor = AutorService.create({"nombre": "A", "apellido": "B", "apodo": "C"})
        libro = LibroService.create({
            "titulo": "Mi Libro", "cantidad": 3,
            "editorial": "Ed", "genero": "Test",
            "sinopsis": "...", "img": "img.jpg",
            "autor": [autor.idAutor]
        })
        _user_id = usuario.idUser
        _libro_id = libro.idLibro
    resp = client.post("/prestamos", json={
        "usuario": _user_id, "libro": [_libro_id]
    }, headers=auth_headers)
    assert resp.status_code == 201
    prestamo_id = resp.get_json()["prestamo"]["id"]
    resp = client.delete(f"/prestamo/{prestamo_id}", headers=auth_headers)
    assert resp.status_code == 204

### TEST USUARIO ###
def test_usuario_create_and_get(client, auth_headers, app):
    resp = client.post("/usuarios", json={
            "user": "VicenCara", "contraseña": "admin123",
            "nombre": "Vicente", "apellido": "Cara",
            "dni": 123409123, "telefono": "2610000000",
            "email": "vicenprest@email.com",
            "rol": "Admin", "img": "img.png", "estado": True
    }, headers=auth_headers)
    assert resp.status_code == 201
    data = resp.get_json()
    usuario_id = data["usuario"]["id"]

    resp = client.get(f"/usuario/{usuario_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["nombre"] == "Vicente"

def test_usuario_update(client, auth_headers, app):
    resp = client.post("/usuarios", json={
        "user": "original", "contraseña": "pass123",
        "nombre": "Original", "apellido": "Uno",
        "dni": 11111111, "telefono": "261111111111",
        "email": "orig@test.com", "rol": "Usuario", "estado": True
    }, headers=auth_headers)
    usuario_id = resp.get_json()["usuario"]["id"]

    resp = client.put(f"/usuario/{usuario_id}", json={
        "nombre": "Modificado"
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["usuario"]["nombre"] == "Modificado"

def test_usuario_delete(client, auth_headers, app):
    resp = client.post("/usuarios", json={
            "user": "VicenCara", "contraseña": "admin123",
            "nombre": "Vicente", "apellido": "Cara",
            "dni": 123409123, "telefono": "2610000000",
            "email": "vicenprest@email.com",
            "rol": "Admin", "img": "img.png", "estado": True
    }, headers=auth_headers)
    data = resp.get_json()
    usuario_id = data["usuario"]["id"]

    resp = client.delete(f"/usuario/{usuario_id}", headers=auth_headers)
    assert resp.status_code == 204

def test_usuario_unauthorized(client):
    resp = client.put("/usuario/1", json={"nombre": "X"})
    assert resp.status_code == 401

    resp = client.delete("/usuario/1")
    assert resp.status_code == 401

### TEST RESEÑA ###
def test_reseña_create_and_get(client, auth_headers, app):
    with app.app_context():
        from main.services import UsuarioService, AutorService, LibroService
        usuario = UsuarioService.create({
            "user": "resuser", "contraseña": "pass123",
            "nombre": "Res", "apellido": "User",
            "dni": 11111111, "telefono": "2611111111",
            "email": "resuser@test.com", "rol": "Usuario", "estado": True
        })
        autor = AutorService.create({"nombre": "A", "apellido": "B", "apodo": "C"})
        libro = LibroService.create({
            "titulo": "Libro Reseña", "cantidad": 5,
            "editorial": "Ed", "genero": "Test",
            "sinopsis": "...", "img": "r.jpg",
            "autor": [autor.idAutor]
        })
        _uid = usuario.idUser
        _lid = libro.idLibro
    resp = client.post("/reseñas", json={
        "usuario": _uid, "libro": _lid,
        "fecha": "15-06-2026", "descripcion": "Buen libro",
        "valoracion": "5"
    }, headers=auth_headers)
    assert resp.status_code == 201
    reseña_id = resp.get_json()["reseña"]["id"]

    resp = client.get(f"/reseña/{reseña_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["descripcion"] == "Buen libro"

def test_reseña_list(client, auth_headers, app):
    with app.app_context():
        from main.services import UsuarioService, AutorService, LibroService
        usuario = UsuarioService.create({
            "user": "rl", "contraseña": "p", "nombre": "R", "apellido": "L",
            "dni": 22222222, "telefono": "2612222222",
            "email": "rl@test.com", "rol": "Usuario", "estado": True
        })
        autor = AutorService.create({"nombre": "A", "apellido": "B", "apodo": "C"})
        libro = LibroService.create({
            "titulo": "L", "cantidad": 2, "editorial": "E",
            "genero": "G", "sinopsis": "...", "img": "x.jpg",
            "autor": [autor.idAutor]
        })
        _uid = usuario.idUser
        _lid = libro.idLibro
    client.post("/reseñas", json={
        "usuario": _uid, "libro": _lid,
        "fecha": "15-06-2026", "descripcion": "A", "valoracion": "4"
    }, headers=auth_headers)
    client.post("/reseñas", json={
        "usuario": _uid, "libro": _lid,
        "fecha": "16-06-2026", "descripcion": "B", "valoracion": "5"
    }, headers=auth_headers)
    resp = client.get("/reseñas")
    assert resp.status_code == 200
    assert resp.get_json()["total"] >= 2

def test_reseña_update(client, auth_headers, app):
    with app.app_context():
        from main.services import UsuarioService, AutorService, LibroService
        usuario = UsuarioService.create({
            "user": "rup", "contraseña": "p", "nombre": "R", "apellido": "U",
            "dni": 33333333, "telefono": "2613333333",
            "email": "rup@test.com", "rol": "Usuario", "estado": True
        })
        autor = AutorService.create({"nombre": "A", "apellido": "B", "apodo": "C"})
        libro = LibroService.create({
            "titulo": "LU", "cantidad": 2, "editorial": "E",
            "genero": "G", "sinopsis": "...", "img": "x.jpg",
            "autor": [autor.idAutor]
        })
        _uid = usuario.idUser
        _lid = libro.idLibro
    resp = client.post("/reseñas", json={
        "usuario": _uid, "libro": _lid,
        "fecha": "15-06-2026", "descripcion": "Original", "valoracion": "3"
    }, headers=auth_headers)
    reseña_id = resp.get_json()["reseña"]["id"]

    resp = client.put(f"/reseña/{reseña_id}", json={
        "descripcion": "Actualizada"
    }, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["reseña"]["descripcion"] == "Actualizada"

def test_reseña_delete(client, auth_headers, app):
    with app.app_context():
        from main.services import UsuarioService, AutorService, LibroService
        usuario = UsuarioService.create({
            "user": "rdel", "contraseña": "p", "nombre": "R", "apellido": "D",
            "dni": 44444444, "telefono": "2614444444",
            "email": "rdel@test.com", "rol": "Usuario", "estado": True
        })
        autor = AutorService.create({"nombre": "A", "apellido": "B", "apodo": "C"})
        libro = LibroService.create({
            "titulo": "LD", "cantidad": 2, "editorial": "E",
            "genero": "G", "sinopsis": "...", "img": "x.jpg",
            "autor": [autor.idAutor]
        })
        _uid = usuario.idUser
        _lid = libro.idLibro
    resp = client.post("/reseñas", json={
        "usuario": _uid, "libro": _lid,
        "fecha": "15-06-2026", "descripcion": "Del", "valoracion": "2"
    }, headers=auth_headers)
    reseña_id = resp.get_json()["reseña"]["id"]
    resp = client.delete(f"/reseña/{reseña_id}", headers=auth_headers)
    assert resp.status_code == 204

def test_reseña_unauthorized(client):
    resp = client.post("/reseñas", json={
        "usuario": 1, "libro": 1,
        "fecha": "15-06-2026", "descripcion": "X", "valoracion": "1"
    })
    assert resp.status_code == 401

    resp = client.put("/reseña/1", json={"descripcion": "X"})
    assert resp.status_code == 401

    resp = client.delete("/reseña/1")
    assert resp.status_code == 401

### TEST NOTIFICACION ###
def test_notificacion_create_and_get(client, auth_headers, app):
    with app.app_context():
        from main.services import UsuarioService
        usuario = UsuarioService.create({
            "user": "notif", "contraseña": "p", "nombre": "N", "apellido": "U",
            "dni": 55555555, "telefono": "2615555555",
            "email": "notif@test.com", "rol": "Usuario", "estado": True
        })
        _uid = usuario.idUser
    resp = client.post("/notificaciones", json={
        "usuario": _uid, "descripcion": "Notificacion de prueba"
    }, headers=auth_headers)
    assert resp.status_code == 201
    notif_id = resp.get_json()["notificacion"]["id"]

    resp = client.get(f"/notificacion/{notif_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["descripcion"] == "Notificacion de prueba"

def test_notificacion_list(client, auth_headers, app):
    with app.app_context():
        from main.services import UsuarioService
        usuario = UsuarioService.create({
            "user": "nl", "contraseña": "p", "nombre": "N", "apellido": "L",
            "dni": 66666666, "telefono": "2616666666",
            "email": "nl@test.com", "rol": "Usuario", "estado": True
        })
        _uid = usuario.idUser
    client.post("/notificaciones", json={
        "usuario": _uid, "descripcion": "A"
    }, headers=auth_headers)
    client.post("/notificaciones", json={
        "usuario": _uid, "descripcion": "B"
    }, headers=auth_headers)
    resp = client.get("/notificaciones", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.get_json()["total"] >= 2

def test_notificacion_delete(client, auth_headers, app):
    with app.app_context():
        from main.services import UsuarioService
        usuario = UsuarioService.create({
            "user": "ndel", "contraseña": "p", "nombre": "N", "apellido": "D",
            "dni": 77777777, "telefono": "2617777777",
            "email": "ndel@test.com", "rol": "Usuario", "estado": True
        })
        _uid = usuario.idUser
    resp = client.post("/notificaciones", json={
        "usuario": _uid, "descripcion": "Temp"
    }, headers=auth_headers)
    notif_id = resp.get_json()["notificacion"]["id"]
    resp = client.delete(f"/notificacion/{notif_id}", headers=auth_headers)
    assert resp.status_code == 204

def test_notificacion_unauthorized(client):
    resp = client.post("/notificaciones", json={
        "usuario": 1, "descripcion": "X"
    })
    assert resp.status_code == 401

    resp = client.delete("/notificacion/1")
    assert resp.status_code == 401

### TEST GUARDADO ###
def test_guardado_create_and_delete(client, auth_headers, app):
    with app.app_context():
        from main.services import UsuarioService, AutorService, LibroService
        usuario = UsuarioService.create({
            "user": "guard", "contraseña": "p", "nombre": "G", "apellido": "U",
            "dni": 88888888, "telefono": "2618888888",
            "email": "guard@test.com", "rol": "Usuario", "estado": True
        })
        autor = AutorService.create({"nombre": "A", "apellido": "B", "apodo": "C"})
        libro = LibroService.create({
            "titulo": "Guardable", "cantidad": 1,
            "editorial": "E", "genero": "G",
            "sinopsis": "...", "img": "g.jpg",
            "autor": [autor.idAutor]
        })
        _uid = usuario.idUser
        _lid = libro.idLibro
    resp = client.post("/guardados", json={
        "libro": _lid
    }, headers=auth_headers)
    assert resp.status_code == 201
    guardado_id = resp.get_json()["guardado"]["id"]

    resp = client.delete(f"/guardado/{guardado_id}", headers=auth_headers)
    assert resp.status_code == 204

def test_guardado_list(client, auth_headers, app):
    resp = client.get("/guardados", headers=auth_headers)
    assert resp.status_code == 200

def test_guardado_unauthorized(client):
    resp = client.post("/guardados", json={"libro": 1})
    assert resp.status_code == 401

    resp = client.delete("/guardado/1")
    assert resp.status_code == 401