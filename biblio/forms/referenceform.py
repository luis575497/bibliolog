from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import Email, InputRequired 
from wtforms.widgets import TextArea

from datetime import datetime

class ReferenceForm(FlaskForm):
    activity = SelectField(u'Actividad realizada', choices=
                            [('Asesoría para registrar publicaciones científicas', 'Asesoría para registrar publicaciones científicas'),
                             ('Asesoría en el uso de equipos', 'Asesoría en el uso de equipos'),
                             ("Asesoría sobre publicación de trabajos de titulación","Asesoría sobre publicación de trabajos de titulació"),
                             ("Búsqueda de documentos en recursos digitales y estanterías","Búsqueda de documentos en recursos digitales y estanterías"),
                             ("Asesoría en el Sistema de Control de Similitudes","Asesoría en el Sistema de Control de Similitude"),
                             ("Asesoría en el uso de los recursos digitales","Asesoría en el uso de los recursos digitales"),
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