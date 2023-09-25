from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField 
from wtforms.validators import InputRequired 
from biblio import font_awesome

from datetime import datetime
    
class StatsDateForm(FlaskForm):
    end_date = DateField('Hasta', default=datetime.today, validators=[InputRequired ()])
    start_date = DateField('Desde', validators=[InputRequired ()])
    submit = SubmitField('Buscar')