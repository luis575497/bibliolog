from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField, PasswordField
from wtforms.validators import Email, InputRequired 
from wtforms.widgets import TextArea
from . import font_awesome

from datetime import datetime

class Reference(FlaskForm):
    activity = SelectField(u'Actividad realizada', choices=
                            [('Asesoría para registrar publicaciones científicas', 'Asesoría para registrar publicaciones científicas'),
                             ('Asesoría en el uso de equipos: escáner, computadoras, pantallas  cubículos y proyector mediateca', 'Asesoría en el uso de equipos: escáner, computadoras, pantallas  cubículos y proyector mediateca'),
                             ("Asesoría sobre trabajos de titulación: formato, acceso restringido, cambios de archivo","Asesoría sobre trabajos de titulación: formato, acceso restringido, cambios de archivo"),
                             ("Búsqueda de documentos en: repositorio, catálogo, bases digitales y estanterías","Búsqueda de documentos en: repositorio, catálogo, bases digitales y estanterías"),
                             ("Asesoría en el Sistema de Control de Similitudes: ingreso, creación de cuentas, eliminación y otros","Asesoría en el Sistema de Control de Similitudes: ingreso, creación de cuentas, eliminación y otros"),
                             ("Asesoría en el uso de los recursos digitales: bases, catálogo, repositorio, gestores, biblioteca","Asesoría en el uso de los recursos digitales: bases, catálogo, repositorio, gestores, biblioteca"),
                             ("Emisión de certificado de 60 horas","Emisión de certificado de 60 horas"),
                             ("Orientación para emisión de certificados de no adeudar","Orientación para emisión de certificados de no adeudar"),
                             ("Referencia especializada","Referencia especializada"),])
    details = StringField(u'Detalle', widget=TextArea())
    email = StringField('Correo del usuario', validators=[InputRequired ("Ingrese una dirección de correo electrónico"), Email("Este campo requiere una dirección de correo válida")])
    submit = SubmitField('Crear')
    update = SubmitField('Actualizar')
    date = DateField('Fecha', default=datetime.today)
    user_type = SelectField(u'Tipo de usuario', choices=
                            [('estudiantes', 'Estudiante'), 
                             ('docente-investigador', 'Docente o Investigador'), 
                             ('general', 'Público Externo'),
                             ("administrativo", "Adminstrativo")]) 
    modality = SelectField(u'Modalidad', choices=
                            [('presencial', 'Presencial'), 
                             ('virtual', 'Virtual'),]) 
    
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
    
class StatsDateForm(FlaskForm):
    end_date = DateField('Fecha', default=datetime.today, validators=[InputRequired ()])
    start_date = DateField('Fecha', validators=[InputRequired ()])
    submit = SubmitField('Buscar')