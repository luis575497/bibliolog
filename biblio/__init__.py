from flask import Flask
from flask_bcrypt import Bcrypt

from .extensions import db, login_manager, bcrypt, avatars, font_awesome, admin, mail
from .reference import reference
from .auth import login
from .stats import stats

import os

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='anything-hard-to-guess',
        SQLALCHEMY_DATABASE_URI= "sqlite:///db.sqlite3",
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USERNAME = 'biblioteca@ucuenca.edu.ec',
        MAIL_PASSWORD = 'zgjinssdybxlneot',
        MAIL_USE_TLS = True
    )

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

    #Crear tablas
    from . import models
    with app.app_context():
        db.create_all()

    #Blueprints (Módulos)
    app.register_blueprint(reference)
    app.register_blueprint(login)
    app.register_blueprint(stats)
    
    return app