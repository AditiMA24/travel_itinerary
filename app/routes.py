from flask import render_template, request, flash, redirect, url_for, session
from app import app
from app.forms import LoginForm
# from requests import requests
import requests 
import os
import openai
import json
import pandas as pd

openai.api_key = ""




@app.route('/')
@app.route('/index')
def index():
    # user = {'name': 'Gby'}
    return render_template('index.html', title='Home') #,user=user



# ##Imports to generate itinerary
# pip install openai
import pandas as pd
import requests
import time
from datetime import date, time, datetime
from datetime import datetime, timedelta
import os
import openai
import spacy

##KEYS
openai.api_key = ""
openai.Model.list();
dist_key="ScsWl6XfkOpZd2KHCATUMQpsHcNtX"


#####Defining some useful functions that will be used
### NLP Function
# pip istall spacy
# pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz
adventurous_trip_words = ["Exploration", "Adventure","Trekking","Hiking","Mountaineering",
                          "Climbing","Rafting","Canyoning","Skydiving","Bungee jumping",
                          "Paragliding","Zip-lining","Safari", "Wildlife","Camping",
                          "Backpacking","Off-roading","Cycling","Scuba diving","Snorkeling",
                          "Early-morning", "ride", "thrilling", "trek", "hike", "Flyboarding","Motorcycle",
                          "water sport", "hot air balloon", "jet ski"]

nature_trip_words = ["Nature","National Park","Nature Reserve","Wilderness","Forest","Mountain",
                     "Waterfall", "Lake","River","Beach","Island","Countryside", "Flora","Fauna",
                     "Ecotourism","Botanical Garden", "Conservation Area", "Stargazing", "Sunrise",
                     "Early-morning","Sunset"]

religion_trip_words = [ "Pilgrimage","Religious", "Sacred","Temple","Church","Mosque",
                       "Synagogue","Shrine","Monastery","Cathedral","Gurdwara","Ashram",
                       "Holy","Prayer","Devotion","Worship","Spiritual","Divine","Pious","Ritual"]

history_trip_words = ["Historical","History","Heritage","Ancient","Archaeological","Museum","Palace",
                      "Castle","Fort","Monument","Ruins","Landmark","Battlefield","Civilization",
                      "Artefact","Antiquity","Cultural","Architecture","Artifact", "Exhibition",
                      "Manuscript","Colonial","Revolution","Revolutionary","Dynasty","Epoch",
                      "Medieval","Renaissance","Inscription","Decipher","Discovery","Archive",
                      "Historiography","Empire","Kingdom","Civilization","Preservation", "Excavation",
                      "World War","Independence","Biography","Historian","Anthropology","architecture",
                      "tradition"]


art_trip_words = ["Art","Culture", "Contemporary","Exhibition","Gallery","Museum","Performance",
                     "Theater","Music","Dance","Film","Literature","Poetry","Sculpture","Painting",
                     "Photography","Installation","Street art","Graffiti","Street performance",
                     "Fashion","Design","Architecture","Cuisine","Craft","Festival","Street fair",
                     "Concert","Workshop","Artistic","Creative","Expression","Cultural heritage",
                     "Cultural exchange","Multicultural","Artisan","Artwork","Digital art","Contemporary dance",
                     "Live music","Artistic performance","Cultural event","Artistic expression","Art festival",
                     "Cultural center","Contemporary theater","Art installation","Public art","Performance art", 
                     "Cultural celebration","light","show"]

# Load a pre-trained NLP model
nlp = spacy.load("en_core_web_sm")


# Define the broad categories and their respective keyword lists
categories = {
    'adventure': adventurous_trip_words,
    'nature': nature_trip_words,
    'religion': religion_trip_words,
    'history': history_trip_words,
    'art': art_trip_words
}

# Initialize category scores
category_scores = {category: 0 for category in categories}

# Function to categorize a paragraph into categories
def categorize_paragraph(paragraph, categories):
    doc = nlp(paragraph)
    
    # Calculate the category scores based on keywords or patterns
    for token in doc:
        for category, keywords in categories.items():
            if token.text.lower() in [keyword.lower() for keyword in keywords]:
                category_scores[category] += 1
    
    # Determine the highest scoring categories
    highest_score = max(category_scores.values())
    predicted_categories = [category for category, score in category_scores.items() if score == highest_score]
    
    return predicted_categories



def preference_check(category,preference):
  words =preference.replace(",", "").split()
  return any(element in words for element in category)




## Distance Matrix function
### Obtain the distance and time between the first and the following place
def distance_API(origin_point, destination_point):
    if origin_point!=destination_point:
        origin,destination=origin_point, destination_point
        distance_url =f"https://api.distancematrix.ai/maps/api/distancematrix/json?origins="+origin+"&destinations="+destination+"&key="+dist_key
        r = requests.get(distance_url)
        dist_result=r.json()['rows'][0]['elements'][0]
        if dist_result['status']=='ZERO_RESULTS':
            dist_result_set.append('None') 
            time_result_set.append('None')
        elif dist_result['status']=='OK':
            dist_result_set.append(dist_result['distance']['text'])
            time_result_set.append(dist_result['duration']['text'])
    else:
        dist_result_set.append('None') 
        time_result_set.append('None')



 ##Extract information and append to the dataframe
def time_to_decimal(time_str):
    if time_str== 'None':
        return None
    parts = time_str.split()
    hours, mins = 0, 0
    for i, part in enumerate(parts):
        if part.isdigit() and i < len(parts) - 1:
            if parts[i + 1].startswith('hour'):
                hours = int(part)
            elif parts[i + 1].startswith('min'):
                mins = int(part)
            else:
                return None
    return round(hours + mins / 60, 3)



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
        
        place= format(session['Destination'])
        duration=2 #this part will become a variable
        preference="histroy" #this part will become a variable

        
        # initialize
        value=40
        iter=0
        max_iter=20
        count=[100 for _ in range(duration)]

        while any(element > value for element in count)==True:
            if iter<max_iter: 
            
                #Preference Loop starts here
                while pref_count<70 and pref_iter<max_iter: 
                    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": "You are a chatbot"},
                            {"role": "user", "content": f"Generate an itineary for a {duration} trip to {place}."},
                            {"role": "user", "content": f"I am only interested in {preference}. "},
                            {"role": "user", "content": "Format the result in such a way that, 1. Capitalize AM and PM. 2. Separate the time and description by a colon."},
                            {"role": "user", "content": "3. Print the addresses at the end of each suggestion but strictly on the same line. The address is one that I must search on Google maps "},
                            {"role": "user", "content": "4. The address should be followed by the latitude and longitude within brackets. "},
                            {"role": "user", "content": "Each suggestion and address needs to be on the same line. Here is an example that you should strictly follow"},
                            {"role": "user", "content": "10:30 AM: Head to the Kolukkumalai Tea Estate, one of the highest tea plantations in the world. Address: Kolukkumalai Tea Estate, P.O, Kannan Devan Hills, Kerala. (Latitude: 27.1750° N, Longitude: 78.0422° E)"},
                            {"role": "user", "content": "7:00 PM: Athirappilly Road, Pariyaram, Kerala 680724. (Latitude: 10.2792° N, Longitude: 76.5674° E)"},
                        ]
                    )

                    result = ''
                    for choice in response.choices:
                        result += choice.message.content


                    ##Step 2: Create a Dataframe
                    #convert paragraph result to list with one sentence as an element
                    my_list = [result]
                    my_list=my_list[0].replace('\n\n','\n').split('\n') 

                    #keep element only if it contains am or pm
                    itinerary=[]
                    for i in range(len(my_list)):
                        if ('AM:'  in my_list[i]) or ('AM -' in my_list[i]):
                            itinerary=itinerary+[my_list[i]]

                        elif ('PM:' in my_list[i]) or ('PM -' in my_list[i]):
                            itinerary=itinerary+[my_list[i]]

                    # #create a data frame
                    df = pd.DataFrame([item.split('Address: ') for item in itinerary], columns=['Description', 'destination'])

                    if  ('AM: '  in itinerary[0]) or ('PM: ' in itinerary[0]):
                        df[['Time','Description']] = df['Description'].str.split(': ', 1, expand=True)
                    elif ('AM-'  in itinerary[0]) or ('PM-' in itinerary[0]):
                        df[['Time','Description']] = df['Description'].str.split('- ', 1, expand=True)

                    if '-' in df['Time'][0]:
                        df['Time'] = df['Time'].str.replace('- ', '') 

                    # case where no space between number and AM/PM
                    df['Time'] = df['Time'].apply(lambda x: x if ' PM' in x else x.replace('PM', ' PM'))
                    df['Time'] = df['Time'].apply(lambda x: x if ' AM' in x else x.replace('AM', ' AM'))


                    df[['destination','Latitude']] = df['destination'].str.split('Latitude: ', 1, expand=True)
                    df['destination'] = df['destination'].str.replace('(', '')
                    df['Latitude'] = df['Latitude'].str.replace('(', '')
                    df[['Latitude','Longitude']] = df['Latitude'].str.split('Longitude: ', 1, expand=True)
                    df['Longitude'] = df['Longitude'].str.replace(')', '')

                    # Reorder the columns
                    desired_order = ['Time', 'Description', 'destination', 'Latitude','Longitude']
                    df = df.reindex(columns=desired_order)

                    ##Checking the preference match
                    df['category']=df['Description'].apply(lambda x: categorize_paragraph(x, categories))
                    df['preference_check']=df['category'].apply(lambda x: preference_check(x,preference))

                    pref_count=sum(df['preference_check'])/len(df['preference_check'])*100
                    pref_iter=+1
                    ##Preference Loop ends here


                ##Extract duration from GPT result
                df['duration_GPT']=''
                for i in range(len(df['Time'])):
                    if i+1<len(df['Time']):
                        time1=datetime.strptime(df['Time'][i], "%I:%M %p")
                        time2=datetime.strptime(df['Time'][i+1], "%I:%M %p")
                        df['duration_GPT'][i]= (time2-time1).total_seconds()/3600 #time in hours

                df['duration_GPT']=''
                for i in range(len(df['Time'])):
                    if i+1<len(df['Time']):
                        time1=datetime.strptime(df['Time'][i], "%I:%M %p")
                        time2=datetime.strptime(df['Time'][i+1], "%I:%M %p")
                        df['duration_GPT'][i]= ((time2-time1)).total_seconds()/3600 #time in hours //time diff in absolute value
                df['duration_GPT'][len(df['Time'])-1]=0 #last destination in the list

                ##segregate days
                df['day']=1
                for i in range(1,len(df['Time'])):
                    if df['duration_GPT'][i]>0 :
                        df['day'][i+1]=df['day'][i]
                    if df['duration_GPT'][i]<0 :
                        df['day'][i+1] = df['day'][i]+1

                df['duration_GPT']= abs(df['duration_GPT']) #time diff in absolute value 


                ##Identify food related suggestion
                df['has_meal'] = df['Description'].str.contains('lunch|breakfast|dinner', case=False, na=False).astype(int)


                #Destination set
                df['destination_set']=''
                destination_set=list(df['destination'])
                for i in range(len(df['destination'])):
                    df['destination_set'][i]=destination_set


                ### Obtain the distance and time between the first and the following place
                def distance_API(origin_point, destination_point):
                    if origin_point!=destination_point:
                        origin,destination=origin_point, destination_point
                        distance_url =f"https://api.distancematrix.ai/maps/api/distancematrix/json?origins="+origin+"&destinations="+destination+"&key="+dist_key
                        r = requests.get(distance_url)
                        dist_result=r.json()['rows'][0]['elements'][0]
                        if dist_result['status']=='ZERO_RESULTS':
                            dist_result_set.append('None') 
                            time_result_set.append('None')
                        elif dist_result['status']=='OK':
                            dist_result_set.append(dist_result['distance']['text'])
                            time_result_set.append(dist_result['duration']['text'])
                    else:
                        dist_result_set.append('None') 
                        time_result_set.append('None')

                ##Use distance_API function to get data
                dist_result_set=[]
                time_result_set=[]
                for i in range(len(destination_set)):
                    if i+1<len(destination_set):
                        distance_API(destination_set[i], destination_set[i+1])


                ## if food stop, then assign previous place if destination is not given
                for i in range(len(df['Time'])):
                    if df['destination'][i]==None:
                        if ('lunch' or 'breakfast' or 'dinner' or "eat") in df['Description'][i]:
                            df['destination'][i]=df['destination'][i-1]
                            df['Latitude'][i]=df['Latitude'][i-1]
                            df['Longitude'][i]=df['Longitude'][i-1]


                ##Extract information and append to the dataframe
                def time_to_decimal(time_str):
                    if time_str== 'None':
                        return None
                    parts = time_str.split()
                    hours, mins = 0, 0
                    for i, part in enumerate(parts):
                        if part.isdigit() and i < len(parts) - 1:
                            if parts[i + 1].startswith('hour'):
                                hours = int(part)
                            elif parts[i + 1].startswith('min'):
                                mins = int(part)
                            else:
                                return None
                    return round(hours + mins / 60, 3)

                time = [time_to_decimal(t) for t in time_result_set]

                time.append(0) #accounting for no next time at the ending point
                dist_result_set.append(0) #accounting for no next time at the ending point

                df['time_to_next_GPT']= time
                df['distance_to_next_GPT']= dist_result_set

                count_miss = df['distance_to_next_GPT'].isna().groupby(df['day']).sum().tolist()
                count_tot=df.groupby('day').size().tolist()
                count = [(a / b)*100 for a, b in zip(count_miss, count_tot)]
                print(count)
                iter=+ 1
        ###END OF LOOP

        #Update destination set if distance matrix API cannot locate it
        df = df[df.distance_to_next_GPT != 'None']
        df = df.reset_index()
        df=df.drop(['index'], axis=1)
        destination_set=list(df['destination'])
        for i in range(len(df['destination'])):
            df['destination_set'][i]=destination_set

            

        # return f"({itinerary_destination_set},{suggestion_destination_set})"
        return f"{df['destination_set'][0]}"
        





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