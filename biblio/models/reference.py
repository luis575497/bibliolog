from flask_admin.contrib.sqla import ModelView

from ..extensions import admin
from ..extensions import db

class ReferenceModel(db.Model):
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

admin.add_view(ModelView(ReferenceModel, db.session))