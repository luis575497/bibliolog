from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea


class Reference(FlaskForm):
    activity = SelectField(u'Actividad realizada', choices=
                            [('Actividad 1', 'Actividad 1'),
                             ('Actividad 2', 'Actividad 2'),])
    details = StringField(u'Detalles', widget=TextArea())
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Ingresar')
    update = SubmitField('Actualizar')
    date = DateField('Fecha')
    user_type = SelectField(u'Tipo de usuario', choices=
                            [('estudiantes', 'Estudiante'), 
                             ('docente-investigador', 'Docente o Investigador'), 
                             ('general', 'Público Externo')]) 
    modality = SelectField(u'Modalidad', choices=
                            [('presencial', 'Presencial'), 
                             ('virtual', 'Virtual'),]) 