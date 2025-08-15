# Idea: Voice Assistant
# Description:
# For Beginners: Create a basic voice assistant that can perform simple tasks based on voice
# commands. Implement features like responding to "Hello" and providing predefined responses,
# telling the time or date, and searching the web for information based on user queries.
# For Advanced: Develop an advanced voice assistant with natural language processing
# capabilities. Enable it to perform tasks such as sending emails, setting reminders, providing
# weather updates, controlling smart home devices, answering general knowledge questions, and
# even integrating with third-party APIs for more functionality.
# Key Concepts and Challenges:
# 1.Speech Recognition: Learn how to recognize and process voice commands using speech
# recognition libraries or APIs.
# 2.Natural Language Processing (for Advanced): Implement natural language understanding to
# interpret and respond to user queries.
# 3.Task Automation (for Advanced): Integrate with various APIs and services to perform tasks
# like sending emails or fetching weather data.
# 4.User Interaction: Create a user-friendly interaction design that allows users to communicate
# with the assistant via voice commands.
# 5.Error Handling: Handle potential issues with voice recognition, network requests, or task
# execution.
# 6.Privacy and Security (for Advanced): Address security and privacy concerns when handling
# sensitive tasks or personal information.
# 7.Customization (for Advanced): Allow users to personalize the assistant by adding custom
# commands or integrations.

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # speaking speed
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception:
        speak("Sorry, I didn't catch that. Please repeat.")
        return ""
    return query.lower()

def tell_time():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {time}")

def tell_date():
    date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today is {date}")

def search_web(query):
    speak("Searching the web for you")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def get_weather(city):
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] != "404":
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp} degrees Celsius with {weather_desc}")
    else:
        speak("City not found.")

def main():
    speak("Hello, I am your voice assistant. How can I help you?")
    while True:
        query = listen()

        if "time" in query:
            tell_time()
        elif "date" in query:
            tell_date()
        elif "weather" in query:
            speak("Tell me the city name")
            city = listen()
            get_weather(city)
        elif "search" in query:
            speak("What should I search for?")
            term = listen()
            search_web(term)
        elif "exit" in query or "quit" in query:
            speak("Goodbye!")
            break
        elif "hello" in query:
            speak("Hello! How are you?")
        else:
            speak("Sorry, I don't know how to do that yet.")

if __name__ == "__main__":
    main()
