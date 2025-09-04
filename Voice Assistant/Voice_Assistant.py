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

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            print(f"User: {query}")
            return query.lower()
        except Exception:
            speak("Sorry, I did not catch that.")
            return ""

def get_time():
    return datetime.datetime.now().strftime("%I:%M %p")

def get_date():
    return datetime.datetime.now().strftime("%A, %d %B %Y")

def main():
    speak("Hello! I am your voice assistant.")
    while True:
        command = listen()
        if "hello" in command:
            speak("Hello! How can I help you?")
        elif "time" in command:
            speak(f"The current time is {get_time()}")
        elif "date" in command:
            speak(f"Today is {get_date()}")
        elif "search" in command:
            speak("What should I search for?")
            query = listen()
            if query:
                url = "https://www.google.com/search?q=" + query
                speak(f"Here are results for {query}")
                webbrowser.open(url)
        elif "exit" in command or "stop" in command or "bye" in command:
            speak("Goodbye! Have a great day.")
            break
        elif command.strip() != "":
            speak("Sorry, I can only tell you the time, date, or search the web right now.")

if __name__ == "__main__":
    main()
