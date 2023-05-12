from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateTimeField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional

class LoginForm(FlaskForm):
    name = StringField('Name', validators=[Optional()])
    age = IntegerField('Age', validators=[Optional()])
    duration = IntegerField('Duration', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male','Male'), ('female', 'Female'), ('other', 'Other'), ('no' , 'Prefer not to say')], validators=[Optional()])
    destination = StringField('Destination', validators=[DataRequired()]) 
    start = DateTimeField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end = DateTimeField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    preference1= StringField('Prefrence 1', validators=[DataRequired()])
    preference2= StringField('Prefrence 2', validators=[Optional()])
    submit = SubmitField('Submit')