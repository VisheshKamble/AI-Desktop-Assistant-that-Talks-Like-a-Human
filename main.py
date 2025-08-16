
import os
import time
import logging
import speech_recognition as sr
import pyttsx3
import webbrowser
import urllib.parse
import subprocess
import requests
import json
from datetime import datetime, timedelta
import threading

# ---------- CONFIGURATION ----------
WAKE_WORD = "hey vishesh"
EXIT_PHRASES = {"exit", "quit", "stop", "goodbye", "bye"}
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Set your OpenWeatherMap API key in environment
NOTES_FILE = "assistant_notes.txt"

# Website mappings
SITE_KEYWORDS = {
    "google": "https://www.google.com",
    "wikipedia": "https://www.wikipedia.org",
    "cricbuzz": "https://www.cricbuzz.com",
    "instagram": "https://www.instagram.com",
    "github": "https://www.github.com",
    "youtube": "https://www.youtube.com",
    "stackoverflow": "https://stackoverflow.com",
    "reddit": "https://www.reddit.com",
    "twitter": "https://twitter.com",
    "linkedin": "https://www.linkedin.com",
    "gmail": "https://mail.google.com",
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "news": "https://news.google.com",
    "maps": "https://www.google.com/maps",
    "spotify": "https://open.spotify.com",
    "netflix": "https://www.netflix.com",
    "discord": "https://discord.com",
    "telegram": "https://web.telegram.org",
    "codeforces": "https://codeforces.com",
    "geeksforgeeks": "https://www.geeksforgeeks.org",
}

# Application mappings (adjust paths for your system)
APP_COMMANDS = {
    "android studio": r"C:\Program Files\Android\Android Studio\bin\studio64.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
}

# Setup logging
logging.basicConfig(
    filename="assistant.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize TTS
tts = pyttsx3.init()
tts.setProperty("rate", 150)  # Speed of speech
tts.setProperty("volume", 0.9)  # Volume 0-1

def say(text: str):
    """Speak and log text."""
    logging.info(f"Speaking: {text}")
    print(f"[Assistant]: {text}")
    tts.say(text)
    tts.runAndWait()

def listen(device_index=1) -> str:
    """Listen for voice input with optimized settings."""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300  # Adjusted for better sensitivity
    recognizer.dynamic_energy_threshold = False
    try:
        with sr.Microphone(device_index=device_index) as source:
            logging.debug("Listening for command...")
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        text = recognizer.recognize_google(audio, language="en-in")
        logging.info(f"Heard: {text}")
        print(f"[Heard]: {text}")
        return text.lower()
    except sr.WaitTimeoutError:
        logging.debug("No speech detected (timeout).")
    except sr.UnknownValueError:
        logging.warning("Could not understand audio.")
    except sr.RequestError as e:
        logging.error(f"Speech-to-text error: {e}")
    except Exception as e:
        logging.error(f"Listen error: {e}")
    return ""

def get_weather(city: str) -> str:
    """Fetch weather data for a city using OpenWeatherMap API."""
    if not API_KEY:
        return "Weather API key not set. Please configure OPENWEATHER_API_KEY."
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"In {city}, it's {temp} degrees Celsius with {desc}."
    except requests.exceptions.RequestException as e:
        logging.error(f"Weather API error: {e}")
        return "Sorry, I couldn't fetch the weather data."

def save_note(note: str):
    """Save a note to a file with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(NOTES_FILE, "a") as f:
        f.write(f"[{timestamp}] {note}\n")
    return f"Note saved: {note}"

def read_notes() -> str:
    """Read all saved notes."""
    if not os.path.exists(NOTES_FILE):
        return "No notes found."
    with open(NOTES_FILE, "r") as f:
        notes = f.read()
    return notes if notes else "No notes found."

def set_timer(seconds: int):
    """Set a timer that alerts when done."""
    def timer_alert():
        time.sleep(seconds)
        say(f"Timer for {seconds} seconds is up!")
    threading.Thread(target=timer_alert, daemon=True).start()
    return f"Timer set for {seconds} seconds."

def process_command_with_ai(command: str) -> str:
    """Use a mock AI API to interpret complex commands (replace with real AI API)."""
    # Mock AI response (replace with actual API like xAI's API: https://x.ai/api)
    command = command.lower()
    if "weather in" in command:
        city = command.split("weather in")[-1].strip()
        return get_weather(city)
    elif "note" in command or "write down" in command:
        note = command.replace("note", "").replace("write down", "").strip()
        return save_note(note)
    elif "read notes" in command:
        return read_notes()
    elif "timer for" in command:
        try:
            seconds = int(command.split("timer for")[-1].split()[0])
            return set_timer(seconds)
        except ValueError:
            return "Please specify a valid number of seconds."
    return command

def open_website(command: str) -> bool:
    """Handle website-related commands."""
    if command.startswith("play "):
        query = command[5:].replace(" on spotify", "").strip()
        if query:
            say(f"Playing {query} on Spotify")
            encoded = urllib.parse.quote(query)
            webbrowser.open(f"https://open.spotify.com/search/{encoded}")
            return True
    for keyword, url in SITE_KEYWORDS.items():
        if keyword in command:
            say(f"Opening {keyword}")
            webbrowser.open(url)
            return True
    return False

def open_app(command: str) -> bool:
    """Handle application launch commands."""
    for name, path in APP_COMMANDS.items():
        if name in command:
            if os.path.exists(path):
                say(f"Opening {name}")
                try:
                    subprocess.Popen(f'"{path}"', shell=True)
                except Exception as e:
                    say(f"Failed to open {name}")
                    logging.error(f"Launch error for {name}: {e}")
            else:
                say(f"Executable for {name} not found.")
                logging.warning(f"Missing app path: {path}")
            return True
    return False

def handle_command(raw: str):
    """Process voice commands."""
    if not raw:
        return
    raw = raw.lower()
    for ex in EXIT_PHRASES:
        if ex in raw:
            say("Goodbye.")
            exit(0)
    if not raw.startswith(WAKE_WORD):
        logging.debug("Wake word not detected; ignoring.")
        return
    command = raw[len(WAKE_WORD):].strip()
    if not command:
        return
    command = command.replace("launch", "open").replace("start", "open")
    ai_processed = process_command_with_ai(command)
    if ai_processed != command:
        say(ai_processed)
        return
    if open_app(command):
        return
    if open_website(command):
        return
    if "help" in command:
        say("You can say: hey vishesh open Chrome, play Believer on Spotify, check weather in Delhi, take a note, read notes, set timer for 10 seconds, or open YouTube.")
        return
    say(f"Sorry, I didn't understand: {command}")

def main_loop():
    """Main loop for continuous listening."""
    say("Hello Vishesh. Say 'hey vishesh' followed by your command.")
    while True:
        heard = listen(device_index=1)
        if heard:
            handle_command(heard)
        time.sleep(0.2)  # Reduced pause for responsiveness

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        say("Shutting down.")
        logging.info("Assistant terminated by user.")