from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(50))
    details =  db.Column(db.Text())
    fecha = db.Column(db.Date)
    user_type = db.Column(db.String(50))
    email = db.Column(db.String(25), nullable=False)
    modality = db.Column(db.String(50))
