import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
from thefuzz import process
import time

engine = pyttsx3.init()

# Voice settings
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # u can try different voices[1] or voices[0] or voices[2] or voices[3].id
engine.setProperty('rate', 170) # Speed of speech

def speak(text):
    print(f"Assistant: {text}")
    if engine._inLoop:
        engine.endLoop()
    
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.1)

def open_search():
    speak("Opening Google.")
    webbrowser.open("https://www.google.com")

def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {now}")
    
def tell_date():
    today = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today's date is {today}")

def play_music():
    speak("Opening Spotify.")
    webbrowser.open("https://open.spotify.com")

# intent mapping to function - predicting the intent of the user input and executing the corresponding function
COMMAND_MAP = {
    "search google": open_search,
    "open google": open_search,
    "what time is it": tell_time,
    "tell me the time": tell_time,
    "what date is it": tell_date,
    "tell me the date": tell_date,
    "play music": play_music,
    "open spotify": play_music
}

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("\n--- Listening ---")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            text = r.recognize_google(audio).lower()
            print(f"You said: {text}")
            return text
        except Exception:
            print("Error occurred while listening.")
            return "none"  # prevents crashing if it hears nothing or noise in the background

def process_command(user_input):
    if user_input == "none" or len(user_input.strip()) == 0:
        return

    try:
        # for ignoreing random words
        result = process.extractOne(user_input, COMMAND_MAP.keys(), score_cutoff=65)
        
        if result:
            best_match, score = result[0], result[1]
            print(f"Match found: {best_match} ({score}% confidence)")
            action_function = COMMAND_MAP[best_match]
            action_function()
        else:
            speak("I didn't recognize that command.")
            print(f"Ignoring command: {user_input}")
            
    except Exception as e:   # prevents system crash
        print(f"Error processing command: {e}")

if __name__ == "__main__":
    speak("System is now, active.")
    
    while True:
        command = listen()
        process_command(command)