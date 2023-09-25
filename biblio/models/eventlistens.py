from ..extensions import db
from .models import Campus

@db.event.listens_for(Campus.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
     db.session.add(Campus(name='central'))
     db.session.add(Campus(name='paraiso'))
     db.session.add(Campus(name='yanuncay'))
     db.session.add(Campus(name='historico'))
     db.session.commit()