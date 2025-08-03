import os
import time
import speech_recognition as sr
import pyttsx3
import webbrowser
import urllib.parse
import subprocess

# ---------- CONFIGURATION ----------
WAKE_WORD = "hey vishesh"  # prefix required to activate command
EXIT_PHRASES = {"exit", "quit", "stop", "goodbye", "bye"}

# Website keywords -> URL
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

# Local applications (adjust paths to match your system)
APP_COMMANDS = {
    "android studio": r"C:\Program Files\Android\Android Studio\bin\studio64.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    # Example extras you can uncomment and set correct paths:
    # "vs code": r"C:\Users\Dell\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    # "whatsapp": r"C:\Users\Dell\AppData\Local\WhatsApp\WhatsApp.exe",
}
# ------------------------------------

# Initialize TTS
tts = pyttsx3.init()

def say(text: str):
    """Speak and print."""
    print(f"[Assistant]: {text}")
    tts.say(text)
    tts.runAndWait()

def listen(device_index=1):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 200
    recognizer.dynamic_energy_threshold = False
    try:
        with sr.Microphone(device_index=device_index) as source:
            print("Listening for command...")
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=6)
        text = recognizer.recognize_google(audio, language="en-in")
        print(f"[Heard]: {text}")
        return text.lower()
    except sr.WaitTimeoutError:
        print("No speech detected (timeout).")
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Speech-to-text error: {e}")
    except Exception as e:
        print(f"Listen error: {e}")
    return None

def open_website(command: str) -> bool:
    # Spotify play/search
    if command.startswith("play "):
        query = command[5:].replace(" on spotify", "").strip()
        if query:
            say(f"Playing {query} on Spotify")
            encoded = urllib.parse.quote(query)
            webbrowser.open(f"https://open.spotify.com/search/{encoded}")
            return True

    if "spotify" in command and "play" not in command:
        say("Opening Spotify")
        webbrowser.open(SITE_KEYWORDS["spotify"])
        return True

    for keyword, url in SITE_KEYWORDS.items():
        if keyword in command:
            say(f"Opening {keyword}")
            webbrowser.open(url)
            return True
    return False

def open_app(command: str) -> bool:
    for name, path in APP_COMMANDS.items():
        if name in command:
            if os.path.exists(path):
                say(f"Opening {name}")
                try:
                    subprocess.Popen(path)
                except Exception as e:
                    say(f"Failed to open {name}")
                    print(f"Launch error for {name}: {e}")
            else:
                say(f"Executable for {name} not found. Check path.")
                print(f"Missing app path: {path}")
            return True
    return False

def handle_command(raw: str):
    if not raw:
        return

    # Check exit
    for ex in EXIT_PHRASES:
        if ex in raw:
            say("Goodbye.")
            exit(0)

    if not raw.startswith(WAKE_WORD):
        print("Wake word not detected; ignoring.")
        return

    command = raw[len(WAKE_WORD):].strip()
    command = command.replace("launch", "open").replace("start", "open")

    if not command:
        return

    # Try apps
    if open_app(command):
        return
    # Try websites / Spotify
    if open_website(command):
        return
    # Help
    if "help" in command:
        say("You can say things like: hey vishesh open Chrome, hey vishesh play Believer on Spotify, hey vishesh open Android Studio, or hey vishesh open YouTube.")
        return

    # Fallback if nothing matches
    say(f"You said: {command}")

def main_loop():
    say("Hello Vishesh. I am listening. Say 'hey vishesh' before your command.")
    while True:
        heard = listen(device_index=1)  # change if needed
        if heard:
            handle_command(heard)
        time.sleep(0.5)  # small pause between listens

if __name__ == "__main__":
    main_loop()
