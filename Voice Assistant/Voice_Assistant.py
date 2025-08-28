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
import webbrowser

recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    print(f"Assistant: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

def open_website(site_name):
    sites = {
        "youtube": "https://www.youtube.com",
        "gmail": "https://mail.google.com",
        "google": "https://www.google.com",
        "drive": "https://drive.google.com",
        "maps": "https://maps.google.com"
    }
    url = sites.get(site_name.lower())
    if url:
        speak(f"Opening {site_name}")
        webbrowser.open(url)
    else:
        speak("Sorry, I don't know that site.")

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5) # Better accuracy
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            speak(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand.")
            return ""
        except sr.RequestError:
            speak("Service is down.")
            return ""

if __name__ == "__main__":
    while True:
        result = listen()
        # Check for open website commands
        if "open youtube" in result:
            open_website("youtube")
        elif "open gmail" in result:
            open_website("gmail")
        elif "open google" in result:
            open_website("google")
        elif "open drive" in result:
            open_website("drive")
        elif "open maps" in result:
            open_website("maps")
        elif result in ["exit", "bye"]:
            speak("Goodbye!")
            break


