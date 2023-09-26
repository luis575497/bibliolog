from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_avatars import Avatars
from flask_font_awesome import FontAwesome
from flask_admin import Admin
from flask_mailing import Mail


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
avatars= Avatars()
font_awesome = FontAwesome()
admin = Admin()
mail = Mail()
