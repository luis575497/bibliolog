.. Sistema de Referencia Bibliotecaria documentation master file, created by
   sphinx-quickstart on Tue Sep 26 11:08:04 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Sistema de Referencia Bibliotecaria's documentation!
===============================================================

Configuración
-------------------------
Antes de ejecutar el proyecto deberá configurar la conexión con la base de datos en el archivo `config.py` y modificar la propiedad `SQLALCHEMY_DATABASE_URI` en donde:

- `mysql+pymysql` : es el conector de python para mysql.
- `root:admin`: es el usuario y la contraseña  respectivamente.
- `@localhost/estudiantes`: es el host y el nombre de la base de datos.

La base de datos indicada deberá no contener ninguna tabla

.. admonition:: Ejemplo

   Ejemplo de configuración del archivo `config.py`

   .. code-block:: python

    SECRET_KEY='ultrasecret'
    SQLALCHEMY_DATABASE_URI= "sqlite:///db.sqlite3"
    FLASK_ADMIN_SWATCH = 'cerulean'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'user@gmaial'
    MAIL_PASSWORD = 'mypass'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

Instalación
--------------------------
Para poder instalarlo deberá crear un entorno virtual e instalar las dependencia en el archivo `requeriments.txt`


Admin-tools
-------------------------
Para poder editar los datos en la base de datos se podrá acceder al panel de administrador en `/admin`

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   routes



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`