from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class PrimarySearchForm(FlaskForm):
    user_query = StringField('', validators=[DataRequired()])
    submit = SubmitField('Submit')
   