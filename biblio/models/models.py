from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView

from ..extensions import admin
from ..extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80), nullable=False)
    references = db.relationship("Reference", backref="user")
    campus_id =  db.Column(db.Integer, db.ForeignKey("campus.id"))

    def __str__(self):
        return self.name

class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    users = db.relationship("User", backref="campus")

    def __str__(self):
        return self.name

class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(50))
    details =  db.Column(db.Text())
    fecha = db.Column(db.Date)
    user_type = db.Column(db.String(50))
    email = db.Column(db.String(25), nullable=False)
    modality = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __str__(self):
        return self.name

class UserView(ModelView):
    column_hide_backrefs = False

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Campus, db.session))
