import speech_recognition as sr
import logging
import os
import datetime
import webbrowser
import wikipedia
import subprocess
import random 


# This is Logger for the application
LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)

log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=log_path,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


def speak(text):
    """Uses Mac's built-in say command - much more reliable"""
    print(f"Jarvis: {text}")
    subprocess.call(["say", text])


def takeCommand():
    """This function takes command & recognizes it"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-fr")
        print(f"User said: {query}\n")
    except Exception as e:
        logging.info(e)
        print("Say that again please")
        return "none"
    return query


def wish_me():
    """Wish the user according to the time of day"""
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Good Morning Mrs! How are you doing today?")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Mrs! How are you doing today?")
    else:
        speak("Good Evening Mrs! How are you doing today?")
    speak("I am Jarvis. Please tell me how can I help you?")


# Greet once at the start
wish_me()

while True:
    query = takeCommand().lower()

    # Skip if nothing was understood
    if query == "none":
        continue

    # Time
    if "what time" in query or "the time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Mrs, the time is {strTime}")

    # Name
    elif "what is your name" in query or "your name" in query or "what's your name" in query:
        speak("My name is Jarvis")

    # How are you
    elif "how are you" in query:
        speak("I am functioning at full capacity Mrs!")

    # Who made you
    elif "who made you" in query:
        speak("I was created by Leslie Samantha Tientcheu Noumowe, a beautiful girl")

    # Thank you
    elif "thank you" in query:
        speak("You are welcome Mrs! Always happy to help.")

    # Play full playlist
    elif "play music" in query or "play my music" in query or "louange" in query:
        speak("Playing your Louange playlist")
        webbrowser.open("https://www.youtube.com/watch?v=4Srtdtki-f4&list=PLhjKaQiS-NGrzcEA3EGBnSvcofVKXHJxM&autoplay=1")

    # Play a specific song by name
    elif "play" in query:
        song = query.replace("play", "").strip()
        speak(f"Playing {song}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

    # Exit
    elif "exit" in query or "quit" in query or "bye" in query:
        speak("Goodbye Mrs! Have a wonderful day.")
        exit()

    # Calculator
    elif "open calculator" in query or "calculator" in query:
        speak("Opening calculator")
        subprocess.Popen(["open", "-a", "Calculator"])

    # TextEdit
    elif "open notepad" in query or "open textedit" in query:
        speak("Opening TextEdit")
        subprocess.Popen(["open", "-a", "TextEdit"])

    # Google
    elif "open google" in query:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    # Terminal
    elif "open terminal" in query or "open cmd" in query:
        speak("Opening Terminal")
        subprocess.Popen(["open", "-a", "Terminal"])

    # Calendar
    elif "open calendar" in query or "calendar" in query:
        speak("Opening Google Calendar")
        webbrowser.open("https://calendar.google.com")

    # Jokes
    elif "joke" in query:
        jokes = [
            "Why don't programmers like nature? Too many bugs.",
            "I told my computer I needed a break. It said no problem, it will go to sleep.",
            "Why do Java developers wear glasses? Because they don't C sharp."
        ]
        speak(random.choice(jokes))

    # YouTube search
    elif "youtube" in query:
        speak("Opening YouTube for you.")
        query = query.replace("youtube", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    # Facebook
    elif "open facebook" in query:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")

    # Wikipedia
    elif "wikipedia" in query:
        speak("Searching Wikipedia")
        query = query.replace("wikipedia", "").strip()
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except Exception as e:
            logging.info(e)
            speak("I could not find anything on Wikipedia for that.")

    # Fallback
    else:
        speak("I did not understand that. Please try again.")