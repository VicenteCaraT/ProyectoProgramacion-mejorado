import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS

#se inicializa SQL
db = SQLAlchemy()
#Inicializar JWT
jwt = JWTManager()
#se inicializa Flask-mail
mailsender = Mail()

#Inicializa la app , todos lo modulos y recursos
def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:4200"])
    load_dotenv()
    api = Api()
    
    #Si no existe el archivo de base de datos crearlo (solo válido si se utiliza SQLite)
    if not os.path.exists(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')):
        os.mknod(os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME'))

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Uri de configuración de base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+os.getenv('DATABASE_PATH')+os.getenv('DATABASE_NAME')
    db.init_app(app)

    import main.resources as resources
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.LibroResource, '/libro/<id>')
    api.add_resource(resources.LibrosResource, '/libros')
    api.add_resource(resources.PrestamoResource, '/prestamo/<id>')
    api.add_resource(resources.PrestamosResource, '/prestamos')
    api.add_resource(resources.NotificacionResource, '/notificacion/<id>')
    api.add_resource(resources.NotificacionesResource, '/notificaciones')
    api.add_resource(resources.AutorResource, '/autor/<id>')
    api.add_resource(resources.AutoresResource, '/autores')
    api.add_resource(resources.ReseñaResource, '/reseña/<id>')
    api.add_resource(resources.ReseñasResource, '/reseñas')
    api.add_resource(resources.GuardadoResource, '/guardado/<id>')
    api.add_resource(resources.GuardadosResource, '/guardados')
    api.init_app(app)
    #config jwt
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)
    #config mail
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    #Inicializar en app
    mailsender.init_app(app)   
    
    from main.auth import routes
    app.register_blueprint(routes.auth)

    from .logging_config import setup_logging
    setup_logging(app)
    
    # Manejador global de errores
    @app.errorhandler(400)
    def bad_request(error):
        return {"message": "Solicitud invalida" , "error": str(error)}, 400
    
    @app.errorhandler(404)
    def not_found(error):
        return {"message": "Recurso no encontrado"}, 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return {"message": "Método no permitido"}, 405

    @app.errorhandler(500)
    def internal_error(error):
        return {"message": "Error interno del servidor"}, 500

    return app