from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView

from ..extensions import admin
from ..extensions import db, bcrypt

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80), nullable=False)
    references = db.relationship("ReferenceModel", backref="user")
    campus_id =  db.Column(db.Integer, db.ForeignKey("campus.id"))

    def __str__(self):
        return self.name
    
# Vista de Flask-Admin
class UserView(ModelView):
    column_hide_backrefs = False
    forms_columns = ["name","email","password","references","campus_id"]

    #Cambiar la contraseña desde el panel de administrador
    def on_model_change(self, form, model, is_created):
        print("Cambiando contraseña del usuarios")
        model.password = bcrypt.generate_password_hash(form.password.data) 

admin.add_view(UserView(User, db.session))