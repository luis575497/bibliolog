from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import InputRequired 
    
class ProfileForm(FlaskForm):
    username = StringField(u'Correo electrónico', validators=[InputRequired ()])
    password = PasswordField("Password")
    name = StringField(u'Nombres y apellidos', validators=[InputRequired ()])
    submit = SubmitField('Ingresar')
    campus = SelectField(u'Campus', choices=
                            [('central', 'Campus Central'), 
                             ('paraiso', 'Campus Paraíso'), 
                             ('yanuncay', 'Campus Yanuncay'),
                             ('chistorico', 'Campus Centro Histórico')]) 