from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import InputRequired 

from datetime import datetime
 
class LoginForm(FlaskForm):
    username = StringField(u'Correo electrónico', validators=[InputRequired ()], render_kw={"placeholder": "Correo electrónico"})
    password = PasswordField("Password", validators=[InputRequired ()], render_kw={"placeholder": "Password"})
    name = StringField(u'Nombres y apellidos', validators=[InputRequired ()], render_kw={"placeholder": "Nombres y apellidos"})
    submit = SubmitField('Ingresar')
    register = SubmitField('Registrarse')
    campus = SelectField(u'Campus', choices=
                            [('central', 'Campus Central'), 
                             ('paraiso', 'Campus Paraíso'), 
                             ('yanuncay', 'Campus Yanuncay'),
                             ('historico', 'Campus Centro Histórico')]) 
      
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