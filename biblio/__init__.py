from flask import Flask

from .extensions import db
from .routes import reference
import os

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI= "sqlite:///db.sqlite3"
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #Iniciar base de datos
    db.init_app(app)

    #Crear tablas
    from . import models
    with app.app_context():
        db.create_all()

    #Blueprints (Módulos)
    app.register_blueprint(reference)
    
    return app