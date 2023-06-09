from flask import render_template, request, flash, redirect, url_for, session , Response
from app import app
from app.forms import LoginForm



# ##Imports to generate itinerary

#other imports
import pandas as pd
import requests
import time
from datetime import date, time, datetime
from datetime import datetime, timedelta
import os
import openai
import spacy
import numpy as np
import folium
from folium.plugins import MarkerCluster
from IPython.display import display
import re

##KEYS
openai.api_key = ""
openai.Model.list();
dist_key="4Bp1aAWodp70uc0QA2vgC6BScbVdk"




@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home') #,user=user


#####Defining some useful functions that will be used

### NLP Function
###Define set of relevant key words corresponding preference
adventurous_trip_words = ["Exploration", "Adventure", "Trekking", "Hiking", "Mountaineering",
"Climbing", "Rafting", "Canyoning", "Skydiving", "Bungee jumping",
"Paragliding", "Zip-lining", "Safari", "Wildlife", "Camping",
"Backpacking", "Off-roading", "Cycling", "Scuba diving", "Snorkeling",
"Early-morning", "ride", "thrilling", "trek", "hike", "Flyboarding", "Motorcycle",
"water sport", "hot air balloon", "jet ski",
"Malai", "Aruvi", "Maravan", "Jora",
"Anveshan", "Pravas", "Trekking", "Chadhai", "Parvat Chadhana",
"Chadhavana", "Jal-snaan", "Khudai", "Gagan Chhadhna", "Bungee Jumping",
"Paragliding", "Zip-lining", "Safari", "Jangal Jeev", "Camping",
"Pith-pith", "Vanya Yatra", "Cycle Chalana", "Scuba Diving", "Snorkeling",
"Subah-savere", "Sawari", "Thrilling", "Trek", "Hiking", "Flyboarding", "Motorcycle",
"Jal Krida", "Hot Air Balloon", "Jet Ski",
"Pahad", "Jharna", "Nadi", "Dariya", "Samundar", "Dweep", "Vanaspati", "Jeev Jantu",
"Vanya Jeev Abhayaranya"]

nature_trip_words = ["Nature", "National Park", "Nature Reserve", "Wilderness", "Forest", "Mountain",
"Waterfall", "Lake", "River", "Beach", "Island", "Countryside", "Flora", "Fauna",
"Ecotourism", "Botanical Garden", "Conservation Area", "Stargazing", "Sunrise",
"Early-morning", "Sunset", "Wildlife Sanctuary", "Eco-trail",
"Malai", "Aruvi",
"Prakriti", "Rashtriya Udyan", "Prakriti Suraksha Kshetra", "Banjar Zameen", "Parvati",
"Jheel", "Nadi", "Sahil", "Dweep", "Pind", "Gaon", "Van", "Jiv Jantu",
"Paryatan", "Vanopaj", "Sanrakshan Kshetra", "Akash Ganga", "Prabhati",
"Subah", "Suryast", "Jeev Abhayaranya", "Paryavaran Marg"]

religion_trip_words = ["Pilgrimage", "Religious", "Sacred", "Temple", "Church", "Mosque",
"Synagogue", "Shrine", "Monastery", "Cathedral", "Gurdwara", "Ashram",
"Holy", "Prayer", "Devotion", "Worship", "Spiritual", "Divine", "Pious", "Ritual",
"Yatra", "Dargah", "Ghat", "Puja", "Pilgrim", "Aarti",
"Tirthayatra", "Dharmik", "Pavitra", "Prarthana", "Masjid",
"Synagogue", "Stambh", "Math", "Pratishtha", "Punya", "Rasam", "Upasana",
"Adhyatmik", "Divya", "Dharmik", "Pavitratva", "Riti-Rivaj", "Yatra",
"Dargah", "Ghat", "Puja", "Tirthayatri", "Aarti",
"Kovil", "Thiru", "Koil", "Mandir", "Devaru"]

history_trip_words = ["Historical", "History", "Heritage", "Ancient", "Archaeological", "Museum", "Palace", "Castle", "Fort", "Monument", "Ruins", "Landmark", "Battlefield", "Civilization",
"Artefact", "Antiquity", "Cultural", "Architecture", "Artifact", "Exhibition", "Manuscript", "Colonial", "Revolution", "Revolutionary", "Dynasty", "Epoch",
"Medieval", "Renaissance", "Inscription", "Decipher", "Discovery", "Archive", "Historiography", "Empire", "Kingdom", "Civilization", "Preservation", "Excavation",
"World War", "Independence", "Biography", "Historian", "Anthropology", "architecture", "tradition", "Rajbari", "Kote", "Qila", "Purana", "Dynastic", "Sultanate", "Vedic", 
"Sanskrit", "Mughal Empire", "Rajput", "Colonial Era", "British Rule", "Maharaja",
"Maratha Empire", "Gupta Empire", "Vijayanagara Empire", "Mauryan Empire", "Ashoka", "Sultan", "Nawab", "Raja", "Maharani", "Emperor", "Empress", "Princely State",
"Itihasik", "Charitra", "Virasat", "Prachin", "Puratatvya", "Sangrahalaya", "Mahal", "Kila", "Qila", "Purana", "Khandahar", "Yuddhasthal", "Sanskriti",
"Prachin Sthapatya", "Aartika", "Puratatva", "Vibhuti", "Prachinata", "Sanskriti", "Utsav", "Sahitya", "Vastukala", "Rajbhasha", "Samaroh", "Sanskritik",
"Charitra Vigyan", "Samrajya", "Rajya", "Sanskriti", "Sanrakshan", "Kazan", "Svatantrata", "Jeevani", "Itihas-Shastri", "Manav-Shastra", "Vastukala", "Parampara", "Rajbari",
"Kote", "Qila", "Purana", "Rajvanshi", "Sultanat", "Vedic", "Sanskrit", "Mughal Samrajya", "Rajput", "Gulami Kaal", "British Raj", "Maharaja",
"Maratha Samrajya", "Gupta Samrajya", "Vijayanagara Samrajya", "Maurya Samrajya", "Ashoka", "Sultan", "Nawab", "Raja", "Maharani", "Samrat", "Samragyi", "Rajkiya Rajwada"]


art_trip_words = ["Art", "Culture", "Contemporary", "Exhibition", "Gallery", "Museum", "Performance",
"Theater", "Music", "Dance", "Film", "Literature", "Poetry", "Sculpture", "Painting",
"Photography", "Installation", "Street art", "Graffiti", "Street performance",
"Fashion", "Design", "Architecture", "Cuisine", "Craft", "Festival", "Street fair",
"Concert", "Workshop", "Artistic", "Creative", "Expression", "Cultural heritage",
"Cultural exchange", "Multicultural", "Artisan", "Artwork", "Digital art", "Contemporary dance",
"Live music", "Artistic performance", "Cultural event", "Artistic expression", "Art festival",
"Cultural center", "Contemporary theater", "Art installation", "Public art", "Performance art",
"Cultural celebration", "Light", "Show", "Traditional dance", "Classical music", "Folk art",
"Artistic heritage", "Artistic tradition", "Artistic craftsmanship", "Artistic excellence",
"Artistic exploration", "Visual art", "Traditional music", "Artistic community", "Artistic interpretation",
"Artistic collaboration", "Artistic creation", "Artistic expression", "Artistic journey",
"Artistic discovery", "Artistic transformation", "Artistic inspiration",
"Kala", "Sanskriti", "Rangmanch", "Sangeet", "Nritya", "Sahitya", "Murtikala",
"Chitrakala", "Chhayankan", "Bhasha", "Sahitya", "Kala Sangam", "Pramotion",
"Lokrang", "Rasleela", "Abhinaya", "Gaan", "Chhau", "Lavani", "Sangeet Natika",
"Pakhi", "Tala", "Lila", "Swar", "Kalakar", "Kalasrishti", "Kala Darpan",
"Pradarshini", "Nritya Parikrama", "Sanskritik Utsav", "Rangotsav", "Bhumi",
"Sahitya Parishad", "Kala Kendra", "Kala Pradarshini", "Sangeet Mahotsav", "Kalakriti",
"Rasgulla", "Bhog", "Sanskritik Parv", "Abhinay Natya", "Sangeet Sammelan", "Kala Mela",
"Kala Sanskriti"]

# Load a pre-trained NLP model
nlp = spacy.load("en_core_web_sm")


# Define a dictionary with the broad categories and their respective keyword lists
categories = {
    'adventure': adventurous_trip_words,
    'nature': nature_trip_words,
    'religion': religion_trip_words,
    'history': history_trip_words,
    'art': art_trip_words
}

# Initialize category scores by setting it to zero
category_scores = {category: 0 for category in categories}

# Function to categorize a paragraph into categories
def categorize_paragraph(paragraph, categories):
    doc = nlp(paragraph)
    
    # Calculate the category scores based on occurance of keyords in the sentence
    for token in doc:
        for category, keywords in categories.items():
            if token.text.lower() in [keyword.lower() for keyword in keywords]:
                category_scores[category] += 1
    
    # Determine the highest scoring categories
    highest_score = max(category_scores.values())
    predicted_categories = [category for category, score in category_scores.items() if score == highest_score]
    
    return predicted_categories


#Function to check if the preference is as reuested by user
def preference_check(category,preference):
  words =preference.replace(",", "").split() #convert preference from form to a list
  return any(element in words for element in category) #check if the predicted category is as requested by user



#To generate itinerary
@app.route('/questionnaire', methods=['GET', 'POST'])
def questionnaire():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #saving reuired infromation from form in a local database
            session['Destination'] = form.destination.data
            session['Duration'] = form.duration.data
            session['Preference1'] = form.preference1.data
            session['Preference2'] = form.preference2.data

            #saving some global values to use in other routes
            global itinerary
            global place
            global duration

            place= format(session['Destination'])
            duration=int((session['Duration'])) 
            preference1=format(session['Preference1'])
            preference2= format( session['Preference2'])
            preference = f"{preference1}, {preference2}"

            
            try:

                # initialize
                value=40
                iter=0
                max_iter=20
                count=[100 for _ in range(duration)]
                pref_count=0
                pref_iter=0

                while any(element > value for element in count)==True:
                    if iter<max_iter: 
                        # #Preference Loop starts here
                        while pref_count<70 and pref_iter<max_iter: 
                            #Step 1: Query ChatGPT
                            response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                    {"role": "system", "content": "You are a chatbot"},
                                    {"role": "user", "content": f"Generate an itineary for a {duration} day trip to {place}."},
                                    {"role": "user", "content": f"I am only interested in {preference}. "},
                                    {"role": "user", "content": "Format the result in such a way that, 1. Capitalize AM and PM. 2. Separate the time and description by a colon."},
                                    {"role": "user", "content": "3. Print the addresses at the end of each suggestion but strictly on the same line. The address is one that I must search on Google maps "},
                                    {"role": "user", "content": "4. The address should be followed by the latitude and longitude within brackets. "},
                                    {"role": "user", "content": "Each suggestion and address needs to be on the same line. Here is an example that you should strictly follow"},
                                    {"role": "user", "content": "10:30 AM: Head to the Kolukkumalai Tea Estate, one of the highest tea plantations in the world. Address: Kolukkumalai Tea Estate, P.O, Kannan Devan Hills, Kerala. (Latitude: 27.1750° N, Longitude: 78.0422° E)"},
                                    {"role": "user", "content": "7:00 PM: Athirappilly Road, Pariyaram, Kerala 680724. (Latitude: 10.2792° N, Longitude: 76.5674° E)"},
                                    {"role": "user", "content": "Do not number the list"},
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

                            #create a data frame
                            df = pd.DataFrame([item.split('Address: ') for item in itinerary], columns=['Description', 'destination'])

                            #Split sentence by following patterns to multiple variables
                            ##extract time
                            if  ('AM: '  in itinerary[0]) or ('PM: ' in itinerary[0]):
                                df[['Time','Description']] = df['Description'].str.split(': ', expand=True)
                            elif ('AM-'  in itinerary[0]) or ('PM-' in itinerary[0]):
                                df[['Time','Description']] = df['Description'].str.split('- ', expand=True)

                            if '-' in df['Time'][0]:
                                df['Time'] = df['Time'].str.replace('- ', '') 

                            # case where no space between number and AM/PM
                            df['Time'] = df['Time'].apply(lambda x: x if ' PM' in x else x.replace('PM', ' PM'))
                            df['Time'] = df['Time'].apply(lambda x: x if ' AM' in x else x.replace('AM', ' AM'))

                            #extract other information
                            df[['destination','Latitude']] = df['destination'].str.split('Latitude: ', expand=True)
                            df['destination'] = df['destination'].str.replace('(', '')
                            df['Latitude'] = df['Latitude'].str.replace('(', '')
                            df[['Latitude','Longitude']] = df['Latitude'].str.split('Longitude: ', expand=True)
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
                                time1=datetime.strptime(df['Time'][i], "%I:%M %p") #convert the string into time format
                                time2=datetime.strptime(df['Time'][i+1], "%I:%M %p")
                                df['duration_GPT'][i]= (time2-time1).total_seconds()/3600 #time in hours

                        df['duration_GPT']=''
                        for i in range(len(df['Time'])):
                            if i+1<len(df['Time']):
                                time1=datetime.strptime(df['Time'][i], "%I:%M %p")
                                time2=datetime.strptime(df['Time'][i+1], "%I:%M %p")
                                df['duration_GPT'][i]= ((time2-time1)).total_seconds()/3600 #time in hours 
                        df['duration_GPT'][len(df['Time'])-1]=0 #last destination in the list

                        ##segregate days when the time difference turns negative
                        df['day']=1
                        for i in range(1,len(df['Time'])):
                            if df['duration_GPT'][i]>0 :
                                df['day'][i+1]=df['day'][i]
                            if df['duration_GPT'][i]<0 :
                                df['day'][i+1] = df['day'][i]+1

                        df['duration_GPT']= abs(df['duration_GPT']) #time diff in absolute value 

                        ##Identify meal related suggestion
                        df['has_meal'] = df['Description'].str.contains('lunch|breakfast|dinner', case=False, na=False).astype(int)

                        ##Identify trek related suggestion
                        df['has_trek'] = df['Description'].str.contains('trek|trekking|hiking|hike', case=False, na=False).astype(int)

                        #Destination set
                        df['destination_set']=''
                        destination_set=list(df['destination'])
                        for i in range(len(df['destination'])):
                            df['destination_set'][i]=destination_set
                        destination_set_temp=set(destination_set)      

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
                                # If the current part is a digit and there is another part after it
                                if part.isdigit() and i < len(parts) - 1:
                                    if parts[i + 1].startswith('hour'): # If the next part starts with 'hour' save as hours
                                        hours = int(part)
                                    elif parts[i + 1].startswith('min'): #If the next part starts with 'min' save as mins
                                        mins = int(part)
                                    else:
                                        return None
                            return round(hours + mins / 60, 3)

                        #Apply the function
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

                
                
                ###Maximum travel time 5 hours for a day based on this allot time slot to every activity and drop what exceeds the day trip limit:
                df['cumulative_sum'] = df.groupby('day')['time_to_next_GPT'].transform(pd.Series.cumsum)

                threshold =  5 #maximum travel time set to 5 hours
                def time_limit(cum_time):
                    if cum_time<=threshold:
                        return True
                    else:
                        return False
                    
                df['within_time_limit']=df['cumulative_sum'].apply(lambda x: time_limit(x) )

                #Convert time format
                df['Time'] = pd.to_datetime(df['Time'], format='%I:%M %p')
                df['Time'] = df['Time'].dt.time
                df['time_new'] = df['Time'] 

                # Group the DataFrame by the 'day' column
                groups = df.groupby('day')

                #Update time based on travel time + a buffer of 2hours (1 hour buffer if meal stop)
                for day, group in groups:
                    for i in range(1, len(group['Time'])):
                        if group['has_meal'].iloc[i] == 1:
                            original_time = pd.to_datetime(str(group['time_new'].iloc[i])).time()
                            add = 0.75 + group['time_to_next_GPT'].iloc[i-1]
                        elif group['has_trek'].iloc[i] == 1:
                            original_time = pd.to_datetime(str(group['time_new'].iloc[i])).time()
                            add = 2 + group['time_to_next_GPT'].iloc[i-1]
                        else:
                            original_time = pd.to_datetime(str(group['time_new'].iloc[i])).time()
                            add = 1.5 + group['time_to_next_GPT'].iloc[i-1]

                        hours_to_add = int(add)
                        minutes_decimal = add % 1
                        minutes_to_add = int(minutes_decimal * 60) ##adds unrounded minutes 
                        duration = pd.Timedelta(hours=hours_to_add, minutes=minutes_to_add)
                        new_datetime = pd.Timestamp.combine(pd.to_datetime('today'), original_time) + duration
                        new_time = new_datetime.time()
                        
                        # Update the 'time_new' column of the current group
                        group['time_new'].iloc[i] = new_time
                
                        # Update the corresponding rows in the original DataFrame
                        df.at[group.index[i], 'time_new'] = new_time
                
                #Set an upper bound on the visiting hours as 10 pm. Anything beyond this time should be removed
                def check_time(time_str):
                    target_time = pd.to_datetime('22:00:00', format='%H:%M:%S').time()
                    time = pd.to_datetime(time_str, format='%H:%M:%S').time()
                    return time < target_time
                
                # Apply the function 
                df['within_visiting_time_limit'] = df['time_new'].apply(check_time)
                df = df.rename(columns={'within_time_limit': 'within_cum_time_limit'})
                
                #Create a new column 'within_time_limit' which is true if both the visiting and cumulative travel time var condition is true and false otherwise
                df['within_time_limit'] = df['within_visiting_time_limit'] & df['within_cum_time_limit']


                ### If a day has less than 2 suggestions, then generate additional reuslts and print it as note below table
                unique_days = df['day'].unique()

                dfs_by_day = {} 

                # Iterate over the unique days
                for day in unique_days:
                    # Create a DataFrame for the current day using boolean indexing
                    df_day = df[df['day'] == day].copy()
                    dfs_by_day[day] = df_day

                # Iterate over each day and its corresponding DataFrame
                add=[]
                for day, df_day in dfs_by_day.items():
                    # Calculate the sum of 'within_time_limit' for the current day
                    sum_within_time_limit = df_day['within_time_limit'].sum()

                    # Check if the sum is less than 2 for the current day
                    if sum_within_time_limit > 2:
                        # Check if there are at least two destinations in the DataFrame
                        print(f"For Day {day}: Sum of 'within_time_limit' is greater than or equal to 2.")
                    else:
                        first_destination = df_day['destination'].iloc[0]
                        
                        # Check if there are at least two destinations in the DataFrame
                        prompt = f"You are a chatbot\nUser: Give me some undiscovered tourist places to visit in {first_destination}.\nUser: Format: 1. Reply with a one-line answer with only 3-4 places separated by commas. 2. Please do not put a full stop at the end of the result."
                        response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=prompt,
                        max_tokens=50,
                        n=1,
                        stop=None,
                        temperature=0.7,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                    )

                        result2 = response.choices[0].text.strip()
                        print(result2)
                        add += [f"If you wish to visit more places on day {day} of your trip, {result} are some offbeat tourist destinations that should not be missed."]
                add_text = ' '.join(add) #convert list to string

                # Add text below the table if required
                text = f"<p>{add_text}</p>"

                #Save Results for Mapping: destinantions to plot for itinerary purpose
                itinerary=df[df['within_time_limit']==True]
                suggestion = df[(df['within_time_limit'] == False)]
                itinerary_destination_set=list(itinerary['destination'])
                suggestion_destination_set=list(suggestion['destination'])
                itinerary = itinerary.rename(columns={'Time': 'Time_original','time_new': 'Time', 'day': 'Day'})


                # Function to round time to nearest 30 minutes or whole hour (do not want to show 11:43:00. Instead show 12:00:00)
                def round_to_nearest_time(time_str):
                    time = pd.to_datetime(time_str, format='%H:%M:%S').time()
                    minute = time.minute
                    if minute < 30:
                        time = time.replace(minute=0)
                    else:
                        time = time.replace(minute=30)
                    return time

                # Apply the rounding function to the Time column
                itinerary['Time'] = itinerary['Time'].apply(round_to_nearest_time)


                ##Step 3: CREATE map html
                # Create a map centered on India
                india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

                # Create a dictionary to store colors for each day
                color_map = {
                    1: 'blue',
                    2: 'green',
                    3: 'red',
                    4: 'purple',
                    5: 'yellow',
                    6: 'pink',
                    7: 'orange',
                    8: 'cyan',
                    9: 'magenta',
                    10: 'brown',
                    11: 'gray',
                    12: 'olive',
                    13: 'lime',
                    14: 'teal',
                    15: 'navy'
                }

                def extract_coordinates(lat_lon_str):
                    coordinates = re.findall(r'\d+\.\d+', lat_lon_str)
                    return [float(coord) for coord in coordinates]

                destination_data = df[df['within_time_limit'] == True].groupby('day', group_keys=True)[['destination', 'Latitude', 'Longitude']].apply(lambda x: [[row[0], *extract_coordinates(row[1]), *extract_coordinates(row[2])] for _, row in x.iterrows()]).to_dict()

                # Create a marker cluster group
                marker_cluster = MarkerCluster().add_to(india_map)

                # Iterate over the destination_data dictionary
                for day, destinations in destination_data.items():
                    # Get the color for the current day
                    color = color_map.get(day, 'gray')

                    # Create a feature group for markers and polyline of the current day
                    day_group = folium.FeatureGroup(name=f"Day {day}")

                    # Iterate over destinations of the current day
                    for i, (destination, lat, lon) in enumerate(destinations, start=1):
                        # Add a marker with the corresponding color and number
                        folium.Marker(
                            location=[lat, lon],
                            popup=destination,
                            icon=folium.Icon(color=color),
                            tooltip=str(i)  # Set the tooltip as the marker number
                        ).add_to(marker_cluster)  # Add the marker to the marker cluster

                    # Create a polyline for the current day
                    locations = [(lat, lon) for _, lat, lon in destinations]
                    folium.PolyLine(locations, color=color, weight=3, opacity=0.8, smooth_factor=1).add_to(day_group)

                    # Add the feature group to the map
                    day_group.add_to(india_map)

                # Adjust the zoom to fit the markers and polylines
                india_map.fit_bounds(india_map.get_bounds())

                # Add a layer control to the map
                folium.LayerControl().add_to(india_map)

                # Save the map as an HTML file
                india_map.save('my_map.html')
                map_html = india_map._repr_html_() #save map in string format


                #Step 4: Convert dataframe to html
                desired_columns = ['Day','Time', 'Description'] #extract desired columns
                
                html_output = itinerary[desired_columns].to_html(classes='table table-bordered', index=False)
                html_output = html_output.replace('<table', '<table style="background-color: rgb(130, 201, 207)"') 
                html_result = html_output + text + map_html 
                return render_template('output_1.html', html_result=html_result)
            
            except :
            # If there was an error in processing, then save the filled details and user should re-submit
                return render_template('questionnaire.html', title='TellUs', form=form)

    return render_template('questionnaire.html',  title='TellUs', form=form)


#To download
@app.route('/download')
def download_output():
    global itinerary

    desired_columns = ['Day', 'Time', 'Description']  # extract desired columns
    html_output = itinerary[desired_columns].to_html(index=False)
    html_output = html_output.replace('<table', '<table class="table table-bordered table-striped"')
    ##use bootstrap and format the page to download
    html_output = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Generated Itinerary </title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
            <style>
                th {{
                    text-align: left;
                    background-color: #306e85;
                    color: #ffffff;
                    padding: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                {html_output}
            </div>
        </body>
        </html>
    '''.format(html_output=html_output)

    # Set response headers for file download
    headers = {
        'Content-Disposition': 'attachment; filename=output_1.html',
        'Content-Type': 'text/html'
    }

    return Response(html_output, headers=headers)


if __name__ == '__main__':
    app.run()