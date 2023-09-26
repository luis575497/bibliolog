from ..extensions import db, bcrypt
from .models import Campus, User

@db.event.listens_for(Campus.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
     db.session.add(Campus(name='central'))
     db.session.add(Campus(name='paraiso'))
     db.session.add(Campus(name='yanuncay'))
     db.session.add(Campus(name='historico'))
     db.session.commit()

"""
@db.event.listens_for(User.password, 'set', retval=True)
def insert_initial_values(target, value, oldvalue, initiator):
     if value != oldvalue:
        return bcrypt.generate_password_hash(value)
     return value
"""
