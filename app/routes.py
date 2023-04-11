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
import sys
# print(sys.executable)




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
        session['Destination'] = form.destination.data
        session['Start Date'] = form.start.data
        session['End Date'] = form.end.data
        session['duration'] = datetime.strptime(session['End Date'], "%Y/%m/%d") - datetime.strptime(session['Start Date'], "%Y/%m/%d")
        flash("Planning trip to {}" .format(session['Destination']))
        return redirect(url_for('output_0'))
    return render_template('questionnaire.html',  title='TellUs', form=form)



# from requests import requests
 
import requests 
import os
import openai


@app.route('/output_0', methods=['POST'])
def processing():

#     # # Generate the itinerary based on the input data
#     # # This is where you would add your itinerary generation code
#     #Step 1: Ask ChatGPT
    openai.api_key = "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"
    openai.Model.list()
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[ 
        {"role": "system", "content": "You are a chatbot"},
        {"role": "user", "content":  " duration day trip to {}"              
         .format(session['Destination']) ".I like prefrences Generate a complete itenary"}
        ]
)

    result = ''
    for choice in response.choices:
        result += choice.message.content
    print(result)
    # # Render the results template with the generated itinerary
    return render_template('output_0.html',  title='Processing')

# if __name__ == '__main__':
#     app.run(debug=True)
