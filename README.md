# Travel Guide Bot

This project implements a Flask web application that acts as a travel guide bot, leveraging Google's Gemini AI model for generating responses and OpenAI's image generation API for creating images.

## Features

* **AI-powered travel planning:** The bot provides personalized travel plans based on user prompts, considering weather conditions and suggesting relevant activities.
* **Weather information:** The bot fetches weather data for the location mentioned in the prompt using the OpenWeatherMap API.
* **Image generation:** The bot generates images based on user prompts using OpenAI's image generation API.
* **Conversation context:** The bot maintains conversation context, remembering previous responses and using them to provide more relevant and personalized suggestions.

## Setup

1. **Create a `.env` file:**
   * Create a file named `.env` in the project root directory.
   * Add the following lines, replacing the placeholders with your actual API keys:
     ```
     GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
     OPENAI_API_KEY=YOUR_OPENAI_API_KEY
     ```
   * You can obtain your API keys from the Google Cloud Platform and OpenAI websites.

2. **Install dependencies:**
   * Install the required Python packages using pip:
     ```bash
     pip install -r requirements.txt
     ```

## Running the Application

1. **Start the Flask server:**
   * Run the following command in your terminal:
     ```bash
     flask run
     ```
   * The application will be accessible at `http://127.0.0.1:5000/`.

## Usage

1. **Access the web application:** Open the URL `http://127.0.0.1:5000/` in your web browser.
2. **Enter a prompt:** Type your travel-related prompt in the text area and click the "SUBMIT" button.
3. **View the response:** The bot will generate a response based on your prompt, including weather information and travel suggestions.
4. **Generate an image:** Enter a description for the image you want to generate in the "Visualize Your Destination" section and click the "Generate Image" button.

## Code Structure

The project consists of the following files:

* **`app.py`:** The main Flask application file, containing the routes, API calls, and logic for the bot.
* **`templates/index.html`:** The HTML template for the frontend interface.
* **`static/`:** Folder containing static files like CSS and JavaScript.

## Dependencies

* Flask
* google.generativeai
* pyttsx3
* requests
* openai
* dotenv
* os

## Notes

* This project requires an active Google Cloud Platform account and an OpenAI API key.
* The `gemini-1.5-flash` model is used for generating responses. You can explore other Gemini models available on Google Cloud.
* The OpenWeatherMap API key is hardcoded in the `get_weather` function. You can replace it with your own API key.
* The `clean_text` function removes asterisk characters from the response, which might be used for formatting purposes.
* The `session` dictionary stores conversation context, allowing the bot to remember previous responses.

## Future Improvements

* **Error handling:** Implement more robust error handling for API calls and other potential issues.
* **User authentication:** Add user authentication to personalize travel plans and store user preferences.
* **Database integration:** Store conversation history and user data in a database for persistence.
* **More advanced features:** Explore additional features like trip itinerary generation, booking functionality, and integration with other travel-related APIs.
