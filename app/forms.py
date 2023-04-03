from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateTimeField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional

class LoginForm(FlaskForm):
    name = StringField('Name', validators=[Optional()])
    # age = IntegerField('age', validators=[Optional()])
    # gender = SelectField('gender', choices=[('male','Male'), ('female', 'Female'), ('other', 'Other'), ('no' 'Prefer not to say'], validators=[Optional()])
    destination = StringField('Destination', validators=[DataRequired()]) 
    # start = DateTimeField('start', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    # end = DateTimeField('end', format='%Y-%m-%d %H:%M:%S',, validators=[DataRequired()])
    submit = SubmitField('Submit')