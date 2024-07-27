from flask import Flask, request, render_template, jsonify
import google.generativeai as genai
import pyttsx3
import requests
import openai  # Import OpenAI library
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

# Define your API keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') 

genai.configure(api_key=GOOGLE_API_KEY)
openai.api_key = OPENAI_API_KEY

def get_weather(city):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'units': 'metric',
        'appid': 'YOUR WEATHER API'
    }
    response = requests.get(base_url, params=params)
    weather_data = response.json()
    
    if weather_data['cod'] == 200:
        main_weather = weather_data['weather'][0]['main']
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        
        return f'Current weather in {city}: Description: {main_weather} and {description}, Temperature: {temp}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s'
    else:
        return ""

def get_location_name(prompt):
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="You will return the name of the location mentioned. If more than one are mentioned then only return the first location.",
        generation_config=genai.GenerationConfig(
            max_output_tokens=2000,
            temperature=0.9,
        ))
    response = model.generate_content(prompt)
    if response and response._result and response._result.candidates:
        gemini_response = response._result.candidates[0].content.parts[0].text
        return gemini_response.strip()
    else:
        return ""

session = {'context': {'previous_responses': []}}

def get_gemini_response(prompt):
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="""You will respond as a travel planner that plans 
        out one's trips. Mention places specific to the chosen area. **Analyze 
        the weather conditions and inform the user how suitable it is for their 
        trip activities**. If the weather seems perfect, suggest exploring or 
        highlight activities that benefit from the conditions. If the weather 
        is not ideal, suggest alternative activities or recommend rescheduling 
        the trip (depending on severity). DO NOT ask for more information if 
        the user doesn't provide any just give them a generic plan.""",
        generation_config=genai.GenerationConfig(
            max_output_tokens=2000,
            temperature=0.9,
        ))

    weather = get_weather(get_location_name(prompt))

    prompt = prompt + weather
    context = session['context']
    context['previous_responses'].append(prompt)
    response = model.generate_content('\n'.join(context['previous_responses']))

    if response and response._result and response._result.candidates:
        gemini_response = response._result.candidates[0].content.parts[0].text
        context['previous_responses'].append(gemini_response)
        session['context'] = context
        return weather +'\n' + '\n'+ gemini_response 
    else:
        return "No response found"

def clean_text(text):
    return text.replace('*', '')

def generate_image(prompt):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,  
            size="512x512"  
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        return f"Error generating image: {str(e)}"

@app.route('/submit', methods=['POST'])
def submit():
    prompt = request.json.get('prompt')
    if prompt:
        response = get_gemini_response(prompt)
        clean_response = clean_text(response)
        return jsonify(response=clean_response)
    else:
        return jsonify(response="Please enter a prompt.")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_image', methods=['POST'])
def generate_image_route():
    prompt = request.json.get('prompt')
    if prompt:
        image_url = generate_image(prompt)
        return jsonify(image_url=image_url)
    else:
        return jsonify(error="Please enter an image prompt.")
    

if __name__ == '__main__':
    app.run(debug=True)
