from flask import render_template, request, flash, redirect, url_for, session
from app import app
from app.forms import LoginForm





@app.route('/')
@app.route('/index')
def index():
    # user = {'name': 'Gby'}
    return render_template('index.html', title='Home') #,user=user



# ##Imports to generate itinerary
from datetime import datetime
# import requests 
# import os
# import openai



@app.route('/test_output')
def test_output():
    # user = {'name': 'Gby'}
    return render_template('test_output.html', title='test_Output') #,user=user            
    
        

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    form = LoginForm()
    # destination = request.form['destination']
    # # Render the results template with the generated itinerary
    if form.validate_on_submit():
        # session['Destination'] = form.destination.data
        # session['Start Date'] = form.start.data
        # session['End Date'] = form.end.data
        # session['duration'] = datetime.strptime(session['End Date'], "%Y/%m/%d") - datetime.strptime(session['Start Date'], "%Y/%m/%d")
        flash('Login requested for'.format(
            form.destination.data))
        
        # return redirect(url_for('test_output'))
        # return redirect(url_for('output'))
        # flash('Login requested for {}'.format(
            # form.name.data))   
        # return redirect(url_for('index'))

    return render_template('questionnaire.html',  title='TellUs', form=form)




@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    if form.validate_on_submit():

        session['Destination'] = form.destination.data
        session['Start Date'] = form.start.data
        session['End Date'] = form.end.data
        session['duration'] = datetime.strptime(session['End Date'], "%Y/%m/%d") - datetime.strptime(session['Start Date'], "%Y/%m/%d")
        # process the form data and present the output
        flash('Login requested for {}'.format(
            session['Destination']))

        # return render_template('output.html', destination=session['Destination'], start_date=session['Start Date'], end_date=session['End Date'])
    # return render_template('form.html', form=form)

# if __name__ == '__main__':
#     app.run()


# @app.route('/submit_form', methods=['POST'])
# def submit_form():
#     form = LoginForm()
#     # Get input data from the form
#     destination = request.form['destination']
#     duration = datetime.strptime(request.form['end'], "%Y/%m/%d") - datetime.strptime(request.form['start'], "%Y/%m/%d")
#     # age = request.form['Age']
#     # gender = request.form['Gender']
#     start = request.form['Start Date']
#     end = request.form['End Date']
    # prefrences=request.form['Prefrences']

    

# #     # # Generate the itinerary based on the input data
# #     # # This is where you would add your itinerary generation code
# #     #Step 1: Ask ChatGPT
#     openai.api_key = "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"
#     openai.Model.list()
#     response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#             {"role": "system", "content": "You are a chatbot"},
#             {"role": "user", "content": duration "day trip to" destination".I like "prefrences "Generate a complete itenary"},
#         ]
# )

#     # result = ''
#     # for choice in response.choices:
#     #     result += choice.message.content

#     # # Render the results template with the generated itinerary
    # return render_template('submit_form.html',  title='Processing')

# if __name__ == '__main__':
#     app.run(debug=True)
