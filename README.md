**Travel Itinerary Generator**

**Description**
The Travel Itinerary Generator is a project that helps users create personalized travel itineraries based on their preferences. It takes into account factors such as destination, interests, and time duration to generate an itinerary that includes recommended places to visit, activities to do, and a map.

**Table of Contents**
1. Installation
2. Usage

**Installation**

git clone https://github.com/AditiMA24/travel_itinerary.git
cd travel_itinerary
python3 -m venv project_venv
project_venv\Scripts\activate
pip install -r requirements.txt
pip install openai
replace the OpenAI key (shared separately)
python -m spacy download en_core_web_sm



**Usage** 

set FLASK_APP=travel_itinerary.py
flask run

Open your web browser and visit http://localhost:3000 to access the Travel Itinerary Generator.
Enter your desired destination, interests, and time duration in the provided input fields.
Click on the "Submit" button to generate a personalized travel itinerary. Incase, no output gets displayed, kindly click the submit button again. (Note: Since we are building on ChatGPT, we not always get expected results, so we have designed  it in such a way that we just need to re-submit the form.)
Explore the generated itinerary that includes recommended places to visit, activities to do, and a map.