from flask import render_template, request, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'Gby'}
    return render_template('index.html', title='Home',user=user)
    # return "Welcome to Travel itinerary Generator!"

# from flask import Flask, render_template, request



# @app.route('/questionnaire', methods=['GET', 'POST'])
# def questionnaire():
#     form = LoginForm()
#     # if form.validate_on_submit():
#     #     flash('Tell us about your trip {}'.format(
#     #         form.username.data, form.remember_me.data))
#     #     return redirect(url_for('index'))
#     return render_template('questionnaire.html',  title='What are you looking for', form=form)


@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    form = LoginForm()
    # # Get input data from the form
    # destination = request.form['destination']
    # # duration = request.form['duration']
    # name =  request.form['Name']
    # # age = request.form['age']
    # # gender = request.form['gender']
    # # destination = StringField('destination', , validators=[DataRequired()]) 
    # # start = request.form['start']
    # # end = request.form['end']

    # # Generate the itinerary based on the input data
    # # This is where you would add your itinerary generation code

    # Render the results template with the generated itinerary
    return render_template('questionnaire.html',  title='TellUs', form=form)

# if __name__ == '__main__':
#     app.run(debug=True)
