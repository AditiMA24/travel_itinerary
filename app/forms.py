from flask_wtf import FlaskForm
from wtforms import DateField, StringField, BooleanField, SubmitField, DateTimeField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional


class LoginForm(FlaskForm):
    name = StringField('', validators=[Optional()], render_kw={"placeholder": "Name"})
    age = IntegerField('', validators=[Optional()], render_kw={"placeholder": "Age"})
    gender = SelectField('', choices=[('', 'Gender'), ('male','Male'), ('female', 'Female'), ('other', 'Other'), ('no' , 'Prefer not to say')], validators=[Optional()],render_kw={"placeholder": "Gender"})
    destination = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Destination *"}) 
    duration = IntegerField('', validators=[DataRequired()], render_kw={"placeholder": "Duration *"})
    # start = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    # end = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    preference1 = SelectField('', choices=[('', 'Preference 1*'), ('adventure','Adventure'), ('history','History'),('art & culture', 'Art & Culture'),('religion','Religion'),('nature','Nature')], validators=[DataRequired()], render_kw={"placeholder": "Preference 1*"})
    preference2 = SelectField('', choices=[('', 'Preference 2'), ('adventure','Adventure'), ('history','History'),('art & culture', 'Art & Culture'),('religion','Religion'),('nature','Nature')], validators=[Optional()], render_kw={"placeholder": "Preference 2"})
    submit = SubmitField('Submit', render_kw={"class": "btn-submit"})

