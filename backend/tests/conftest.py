import pytest
from main import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
        
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    from main.models import UsuarioModel
    from main.repositories import UsuarioRepository
    user = UsuarioModel(
        user="test", nombre="Test", apellido="User",
        dni=12345678, telefono="123456789", email="test@test.com",
        rol="Admin", estado=True
    )
    user.plain_password = "test123"
    UsuarioRepository.save(user)
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity=user)
    return {"Authorization": f"Bearer {token}"}