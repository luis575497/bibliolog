from flask import Flask

from .extensions import db, login_manager, bcrypt, avatars, font_awesome, admin, mail, toolbar
from .reference import reference
from .auth import login
from .stats import stats
from .errors import page_not_found

import os

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #Iniciar base de datos
    db.init_app(app)

    #Cargar el manejo de inicio de sesión
    login_manager.init_app(app)
    
    #Cargar Módulo Bcrypt
    bcrypt.init_app(app)

    #Cargar módulo de avatars
    avatars.init_app(app)

    #Cargar la fuente Awesome
    font_awesome.init_app(app)

    #Iniciar panel de administrador
    admin.init_app(app)

    #Iniciar Flask-Mail
    mail.init_app(app)

    #Toolbar Debug
    toolbar.init_app(app)

    #Registar errores
    app.register_error_handler(404, page_not_found)

    #Crear tablas
    from .models import campus
    with app.app_context():
        db.create_all()

    #Blueprints (Módulos)
    app.register_blueprint(reference)
    app.register_blueprint(login)
    app.register_blueprint(stats)
    
    return app