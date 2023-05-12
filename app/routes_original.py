from flask import render_template, request, flash, redirect, url_for, session
from app import app
from app.forms import LoginForm
# from requests import requests
import requests 
import os
import openai
import json






@app.route('/')
@app.route('/index')
def index():
    # user = {'name': 'Gby'}
    return render_template('index.html', title='Home') #,user=user



# ##Imports to generate itinerary
from datetime import datetime
import sys
# print(sys.executable)




@app.route('/output_0')
def output_0():
    # user = {'name': 'Gby'}
    return render_template('output_0.html', title='test_Output') #,user=user            
    
        

@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    form = LoginForm()
    # destination = request.form['destination']
    # # Render the results template with the generated itinerary
    if form.validate_on_submit():
        session['Name'] = form.name.data
        session['Destination'] = form.destination.data
        session['Start Date'] = form.start.data
        session['End Date'] = form.end.data
        # session['duration'] = datetime.strptime(session['End Date'], "%Y/%m/%d") - datetime.strptime(session['Start Date'], "%Y/%m/%d")
        # flash("Planning trip to {}" .format(session['Destination']))
        
        # Define the prompt for generating the travel itinerary
        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": "Generate a complete itinerary for a one day trip to" {{(session['Destination'])}} "I prefer adventure. Give me time and destination." },
            {"role": "user", "content": "Format all the place name in uppercase. Capitalize AM and PM in time." },
            {"role": "user", "content": "Separate time and destination with colan" },
        ]
)
        # Extract the generated travel itinerary
        result = ''
        for choice in response.choices:
            result += choice.message.content
        return result
        # itinerary = response.choices[0].text
        # return itinerary
        # flash(itinerary) 

        return redirect(url_for('output_0'), itinerary=itinerary)
    return render_template('questionnaire.html',  title='TellUs', form=form)





# @app.route('/output_1')
# def output_1():
#     # Define the prompt for generating the travel itinerary
#     prompt = "Generate a travel itinerary for a trip to {}" .format(session['Destination'])
#     # Set the parameters for the API request
#     model_engine = "text-davinci-002"
#     temperature = 0.7
#     max_tokens = 1024

#     # Generate the travel itinerary using the OpenAI API
#     response = openai.Completion.create(
#         engine=model_engine,
#         prompt=prompt,
#         temperature=temperature,
#         max_tokens=max_tokens
#     )

#     # Extract the generated travel itinerary
#     itinerary = response.choices[0].text
    
#     flash(itinerary) 

#     # Render the itinerary on a template
#     return render_template('output_1.html', itinerary=itinerary, title='Processing')