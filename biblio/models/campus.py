from flask_admin.contrib.sqla import ModelView

from ..extensions import admin
from ..extensions import db

class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    users = db.relationship("User", backref="campus")

    def __str__(self):
        return self.name

admin.add_view(ModelView(Campus, db.session))


